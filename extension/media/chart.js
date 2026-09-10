// Renders the complexity charts and handles zoom, hover and the colour
// controls. Loaded by both the VS Code webview and the localhost preview.
//
// The data arrives as JSON in #sb-data, written by complexity.py --json.
// Rendering lives here rather than in the extension because zoom has to
// re-render on every interaction.

(function () {
    'use strict';

    /** Mirrors MODELS in python/common/complexity.py. Order matters (neighbours). */
    var MODELS = [
        { name: 'O(1)', f: function () { return 1; } },
        { name: 'O(log n)', f: function (n) { return n > 1 ? Math.log2(n) : 1; } },
        { name: 'O(n)', f: function (n) { return n; } },
        { name: 'O(n log n)', f: function (n) { return n > 1 ? n * Math.log2(n) : n; } },
        { name: 'O(n^2)', f: function (n) { return n * n; } },
        { name: 'O(n^3)', f: function (n) { return Math.pow(n, 3); } },
        { name: 'O(2^n)', f: function (n) { return Math.pow(2, Math.min(n, 60)); } }
    ];

    var DEFAULTS = {
        light: { measured: '#2a78d6', fitted: '#eb6834' },
        dark: { measured: '#3987e5', fitted: '#d95926' }
    };

    var PLOT = { w: 820, h: 360, left: 68, right: 128, top: 18, bottom: 46 };
    var STORE_KEY = 'solvebench.complexity.prefs';

    var data = null;                         // filled in by setUp()
    var host = window.sbHost || {};          // set by the webview shell
    var charts = [];

    // ---------------------------------------------------------------- prefs

    function loadPrefs() {
        var base = { logScale: false, measured: '', fitted: '' };
        try {
            var raw = localStorage.getItem(STORE_KEY);
            if (raw) {
                var saved = JSON.parse(raw);
                Object.keys(base).forEach(function (k) {
                    if (saved[k] !== undefined) { base[k] = saved[k]; }
                });
            }
        } catch (e) {
            // Private windows and cleared site data both land here. Defaults
            // are fine; the controls still work for this session.
        }
        return base;
    }

    function savePrefs() {
        try {
            localStorage.setItem(STORE_KEY, JSON.stringify(prefs));
        } catch (e) { /* nothing worth reporting to the user */ }
    }

    var prefs = loadPrefs();

    function isDark() {
        var b = document.body;
        if (b.classList.contains('vscode-dark') || b.classList.contains('vscode-high-contrast')) {
            return true;
        }
        if (b.classList.contains('vscode-light') || b.dataset.theme === 'light') {
            return false;
        }
        if (b.dataset.theme === 'dark') { return true; }
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    /** The colour actually in force: user override, else the validated default. */
    function activeColor(role) {
        if (prefs[role]) { return prefs[role]; }
        return DEFAULTS[isDark() ? 'dark' : 'light'][role];
    }

    function applyColors() {
        var root = document.body.style;
        ['measured', 'fitted'].forEach(function (role) {
            if (prefs[role]) {
                root.setProperty('--sb-' + role, prefs[role]);
            } else {
                root.removeProperty('--sb-' + role);
            }
        });
    }

    // ---------------------------------------------------------------- maths

    /**
     * Scale factor for c * f(n), fitted in log space. Same method as _best_fit
     * in python/common/complexity.py, so the curve drawn for the winning class
     * is the curve that actually won.
     */
    function fitScale(sizes, values, f) {
        var pts = [];
        for (var i = 0; i < sizes.length; i++) {
            if (values[i] > 0 && isFinite(values[i])) {
                pts.push([sizes[i], values[i]]);
            }
        }
        if (!pts.length) { return 0; }
        var sum = pts.reduce(function (acc, p) {
            return acc + (Math.log(p[1]) - Math.log(f(p[0])));
        }, 0);
        return Math.exp(sum / pts.length);
    }

    /** The fitted class plus its neighbours, for comparison. */
    function classesToDraw(fitted) {
        var i = MODELS.findIndex(function (m) { return m.name === fitted; });
        if (i < 0) { return [fitted]; }
        var picked = [MODELS[i].name];
        if (i > 0) { picked.push(MODELS[i - 1].name); }
        // O(2^n) is unplottable beside the others, so never draw it as context.
        if (i + 1 < MODELS.length && MODELS[i + 1].name !== 'O(2^n)') {
            picked.push(MODELS[i + 1].name);
        }
        return picked;
    }

    function niceTicks(lo, hi, count) {
        var span = hi - lo;
        if (span <= 0) { return [lo]; }
        var raw = span / count;
        var mag = Math.pow(10, Math.floor(Math.log10(raw)));
        var norm = raw / mag;
        var step = (norm >= 5 ? 10 : norm >= 2 ? 5 : norm >= 1 ? 2 : 1) * mag;
        var ticks = [];
        for (var v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) {
            ticks.push(v);
        }
        return ticks;
    }

    /**
     * Ticks for a log axis. Powers of ten alone are too coarse here: the input
     * sizes span barely more than one decade (500..8000), so only 1000 would
     * land inside. Steps of 1, 2 and 5 per decade fill it in.
     */
    function logTicks(lo, hi) {
        var steps = [1, 2, 5];
        var ticks = [];
        var from = Math.floor(Math.log10(lo));
        var to = Math.ceil(Math.log10(hi));
        for (var e = from; e <= to; e++) {
            for (var s = 0; s < steps.length; s++) {
                var v = steps[s] * Math.pow(10, e);
                if (v >= lo * 0.999 && v <= hi * 1.001) { ticks.push(v); }
            }
        }
        // Very narrow ranges can still come up short; the ends always work.
        return ticks.length >= 2 ? ticks : [lo, hi];
    }

    function decimalsFor(max) {
        return max < 1 ? 3 : max < 10 ? 2 : max < 100 ? 1 : 0;
    }

    function fmt(v, decimals) {
        return v.toLocaleString('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    function shortNum(v) {
        if (v === 0) { return '0'; }
        var abs = Math.abs(v);
        if (abs >= 1000) { return Math.round(v).toLocaleString('en-US'); }
        if (abs >= 10) { return v.toFixed(1); }
        if (abs >= 1) { return v.toFixed(2); }
        return v.toFixed(3);
    }

    // ---------------------------------------------------------------- chart

    function Chart(spec) {
        this.spec = spec;                    // {id, sizes, values, fitted, yLabel, unit}
        this.view = null;                    // null = fit to data
        this.svg = spec.svg;
        this.tooltip = spec.tooltip;
        this.zoomState = spec.zoomState;
        this.bindEvents();
    }

    Chart.prototype.dataBounds = function () {
        var s = this.spec;
        var positive = s.values.filter(function (v) { return v > 0; });
        var yLo = prefs.logScale && positive.length
            ? Math.min.apply(null, positive) / 1.6
            : 0;
        return {
            x0: prefs.logScale ? Math.min.apply(null, s.sizes) / 1.3 : 0,
            x1: Math.max.apply(null, s.sizes) * 1.02,
            y0: yLo,
            y1: Math.max.apply(null, s.values) * 1.15 || 1
        };
    };

    Chart.prototype.bounds = function () {
        return this.view || this.dataBounds();
    };

    Chart.prototype.scales = function (b) {
        var innerW = PLOT.w - PLOT.left - PLOT.right;
        var innerH = PLOT.h - PLOT.top - PLOT.bottom;
        var log = prefs.logScale;

        function lin(v, lo, hi) { return (v - lo) / (hi - lo); }
        function lg(v, lo, hi) {
            var s = Math.log(Math.max(v, lo * 1e-6));
            return (s - Math.log(lo)) / (Math.log(hi) - Math.log(lo));
        }
        var fx = log ? lg : lin;
        var fy = log ? lg : lin;

        return {
            innerW: innerW,
            innerH: innerH,
            x: function (v) { return PLOT.left + fx(v, b.x0, b.x1) * innerW; },
            y: function (v) { return PLOT.top + innerH - fy(v, b.y0, b.y1) * innerH; },
            // inverse, for turning a pixel back into a value
            xInv: function (px) {
                var t = (px - PLOT.left) / innerW;
                return log
                    ? Math.exp(Math.log(b.x0) + t * (Math.log(b.x1) - Math.log(b.x0)))
                    : b.x0 + t * (b.x1 - b.x0);
            },
            yInv: function (py) {
                var t = (PLOT.top + innerH - py) / innerH;
                return log
                    ? Math.exp(Math.log(b.y0) + t * (Math.log(b.y1) - Math.log(b.y0)))
                    : b.y0 + t * (b.y1 - b.y0);
            }
        };
    };

    Chart.prototype.render = function () {
        var s = this.spec;
        var b = this.bounds();
        var sc = this.scales(b);
        var log = prefs.logScale;
        var out = [];

        out.push('<defs><clipPath id="clip-' + s.id + '"><rect x="' + PLOT.left +
            '" y="' + PLOT.top + '" width="' + sc.innerW + '" height="' + sc.innerH +
            '"/></clipPath></defs>');

        // y grid + labels
        var yTicks = log ? logTicks(Math.max(b.y0, 1e-9), b.y1) : niceTicks(b.y0, b.y1, 4);
        var yDec = decimalsFor(b.y1);
        yTicks.forEach(function (v) {
            var py = sc.y(v);
            if (py < PLOT.top - 1 || py > PLOT.top + sc.innerH + 1) { return; }
            out.push('<g class="grid"><line x1="' + PLOT.left + '" y1="' + py + '" x2="' +
                (PLOT.left + sc.innerW) + '" y2="' + py + '"/></g>');
            out.push('<text class="tick" x="' + (PLOT.left - 8) + '" y="' + (py + 4) +
                '" text-anchor="end">' + (log ? shortNum(v) : fmt(v, yDec)) + '</text>');
        });

        // x labels: drop any that would collide with the one before it
        var xTicks = log ? logTicks(b.x0, b.x1) : s.sizes.filter(function (n) {
            return n >= b.x0 && n <= b.x1;
        });
        var lastX = -Infinity;
        xTicks.forEach(function (n, i) {
            var px = sc.x(n);
            if (px < PLOT.left - 1 || px > PLOT.left + sc.innerW + 1) { return; }
            if (i !== xTicks.length - 1 && px - lastX < 36) { return; }
            lastX = px;
            out.push('<text class="tick" x="' + px + '" y="' + (PLOT.top + sc.innerH + 18) +
                '" text-anchor="middle">' + (n >= 1000 ? shortNum(n) : n) + '</text>');
        });

        out.push('<line class="axis" x1="' + PLOT.left + '" y1="' + PLOT.top + '" x2="' +
            PLOT.left + '" y2="' + (PLOT.top + sc.innerH) + '"/>');
        out.push('<line class="axis" x1="' + PLOT.left + '" y1="' + (PLOT.top + sc.innerH) +
            '" x2="' + (PLOT.left + sc.innerW) + '" y2="' + (PLOT.top + sc.innerH) + '"/>');

        // curves + measured line, clipped to the plot box
        var drawn = classesToDraw(s.fitted);
        // Sample across the visible range so a curve stays smooth when zoomed.
        var samples = [];
        for (var k = 0; k <= 60; k++) {
            samples.push(sc.xInv(PLOT.left + (k / 60) * sc.innerW));
        }

        var clipped = ['<g clip-path="url(#clip-' + s.id + ')">'];
        drawn.forEach(function (name, idx) {
            var model = MODELS.find(function (m) { return m.name === name; });
            var c = fitScale(s.sizes, s.values, model.f);
            var d = samples.map(function (n, j) {
                return (j ? 'L' : 'M') + sc.x(n).toFixed(1) + ',' + sc.y(c * model.f(n)).toFixed(1);
            }).join(' ');
            clipped.push('<path class="' + (idx === 0 ? 'fit' : 'ref') + '" d="' + d + '"/>');
        });

        clipped.push('<path class="measured" d="' + s.sizes.map(function (n, i) {
            return (i ? 'L' : 'M') + sc.x(n).toFixed(1) + ',' + sc.y(s.values[i]).toFixed(1);
        }).join(' ') + '"/>');
        s.sizes.forEach(function (n, i) {
            clipped.push('<circle class="dot" cx="' + sc.x(n).toFixed(1) + '" cy="' +
                sc.y(s.values[i]).toFixed(1) + '" r="4"/>');
        });
        clipped.push('</g>');
        out.push(clipped.join(''));

        // legend
        var lx = PLOT.left + sc.innerW + 12;
        out.push('<circle class="dot" cx="' + (lx + 9) + '" cy="' + (PLOT.top + 10) + '" r="4"/>');
        out.push('<text class="legend" x="' + (lx + 24) + '" y="' + (PLOT.top + 14) + '">measured</text>');
        drawn.forEach(function (name, idx) {
            var ly = PLOT.top + 30 + idx * 18;
            out.push('<line class="' + (idx === 0 ? 'fit' : 'ref') + '" x1="' + lx +
                '" y1="' + (ly - 4) + '" x2="' + (lx + 18) + '" y2="' + (ly - 4) + '"/>');
            out.push('<text class="legend" x="' + (lx + 24) + '" y="' + ly + '">' + name + '</text>');
        });

        out.push('<text class="axisLabel" x="' + (PLOT.left + sc.innerW / 2) + '" y="' +
            (PLOT.h - 6) + '" text-anchor="middle">input size (n)' +
            (log ? ' — log scale' : '') + '</text>');
        out.push('<text class="axisLabel" transform="translate(14,' +
            (PLOT.top + sc.innerH / 2) + ') rotate(-90)" text-anchor="middle">' +
            s.yLabel + (log ? ' — log scale' : '') + '</text>');

        // one transparent rect on top, so pointer events have a target
        out.push('<rect class="hitTarget" x="' + PLOT.left + '" y="' + PLOT.top +
            '" width="' + sc.innerW + '" height="' + sc.innerH + '"/>');

        this.svg.innerHTML = out.join('');
        this.sc = sc;
        this.b = b;
        this.zoomState.textContent = this.view ? 'zoomed' : '';
        var bar = document.querySelector('.zoomBar [data-zoom="' + s.id + '"][data-act="fit"]');
        if (bar) { bar.disabled = !this.view; }
    };

    Chart.prototype.nearest = function (valueX) {
        var s = this.spec;
        var best = 0;
        var bestD = Infinity;
        s.sizes.forEach(function (n, i) {
            var d = Math.abs(n - valueX);
            if (d < bestD) { bestD = d; best = i; }
        });
        return best;
    };

    Chart.prototype.bindEvents = function () {
        var self = this;
        var svg = this.svg;

        function toSvg(evt) {
            var r = svg.getBoundingClientRect();
            return {
                x: ((evt.clientX - r.left) / r.width) * PLOT.w,
                y: ((evt.clientY - r.top) / r.height) * PLOT.h,
                px: evt.clientX - r.left,
                py: evt.clientY - r.top
            };
        }

        svg.addEventListener('pointermove', function (evt) {
            var p = toSvg(evt);
            if (p.x < PLOT.left || p.x > PLOT.w - PLOT.right) {
                self.tooltip.classList.remove('on');
                return;
            }
            var i = self.nearest(self.sc.xInv(p.x));
            var s = self.spec;
            self.tooltip.innerHTML =
                '<span class="k">n</span> <b>' + s.sizes[i].toLocaleString('en-US') +
                '</b><br><span class="k">' + s.yLabel + '</span> <b>' +
                shortNum(s.values[i]) + '</b>';
            var r = svg.getBoundingClientRect();
            self.tooltip.style.left = (self.sc.x(s.sizes[i]) / PLOT.w) * r.width + 'px';
            self.tooltip.style.top = ((self.sc.y(s.values[i]) / PLOT.h) * r.height - 10) + 'px';
            self.tooltip.classList.add('on');
        });

        svg.addEventListener('pointerleave', function () {
            self.tooltip.classList.remove('on');
        });

        // Wheel zoom needs Ctrl (or Cmd). A bare wheel keeps scrolling the
        // page, which is what a reader expects from a page with two charts on
        // it -- hijacking it traps the scroll.
        svg.addEventListener('wheel', function (evt) {
            if (!evt.ctrlKey && !evt.metaKey) {
                return;                      // let the page scroll
            }
            evt.preventDefault();
            var p = toSvg(evt);
            self.zoomAt(evt.deltaY > 0 ? 1.18 : 1 / 1.18, p.x, p.y);
        }, { passive: false });

        // drag to pan
        var dragging = null;
        svg.addEventListener('pointerdown', function (evt) {
            var p = toSvg(evt);
            if (p.x < PLOT.left || p.x > PLOT.w - PLOT.right) { return; }
            // Without this the drag also starts a text selection across the page.
            evt.preventDefault();
            dragging = { p: p, b: self.bounds() };
            svg.classList.add('panning');
            svg.setPointerCapture(evt.pointerId);
        });
        // Belt and braces for browsers that still begin a selection.
        svg.addEventListener('selectstart', function (evt) { evt.preventDefault(); });
        svg.addEventListener('dragstart', function (evt) { evt.preventDefault(); });
        svg.addEventListener('pointerup', function (evt) {
            dragging = null;
            svg.classList.remove('panning');
            try { svg.releasePointerCapture(evt.pointerId); } catch (e) { /* already gone */ }
        });
        svg.addEventListener('pointermove', function (evt) {
            if (!dragging) { return; }
            var p = toSvg(evt);
            var sc = self.scales(dragging.b);
            var b = dragging.b;
            var log = prefs.logScale;
            if (log) {
                var kx = Math.log(b.x1 / b.x0) * ((p.x - dragging.p.x) / sc.innerW);
                var ky = Math.log(b.y1 / b.y0) * ((p.y - dragging.p.y) / sc.innerH);
                self.view = {
                    x0: b.x0 / Math.exp(kx), x1: b.x1 / Math.exp(kx),
                    y0: b.y0 * Math.exp(ky), y1: b.y1 * Math.exp(ky)
                };
            } else {
                var dx = (b.x1 - b.x0) * ((p.x - dragging.p.x) / sc.innerW);
                var dy = (b.y1 - b.y0) * ((p.y - dragging.p.y) / sc.innerH);
                self.view = {
                    x0: b.x0 - dx, x1: b.x1 - dx,
                    y0: b.y0 + dy, y1: b.y1 + dy
                };
            }
            self.render();
        });

        svg.addEventListener('dblclick', function () {
            self.reset();
        });
    };

    /** Zoom by `factor` about a point in svg coordinates (default: centre). */
    Chart.prototype.zoomAt = function (factor, px, py) {
        var b = this.bounds();
        var log = prefs.logScale;
        var cx = this.sc.xInv(px === undefined ? PLOT.left + this.sc.innerW / 2 : px);
        var cy = this.sc.yInv(py === undefined ? PLOT.top + this.sc.innerH / 2 : py);

        function around(lo, hi, c) {
            if (log) {
                var l = Math.log, e = Math.exp;
                return [e(l(c) - (l(c) - l(lo)) * factor), e(l(c) + (l(hi) - l(c)) * factor)];
            }
            return [c - (c - lo) * factor, c + (hi - c) * factor];
        }
        var nx = around(b.x0, b.x1, cx);
        var ny = around(b.y0, b.y1, cy);
        this.view = {
            // Linear axes start at zero, so that end stays pinned.
            x0: log ? Math.max(nx[0], 1e-9) : Math.max(nx[0], 0),
            x1: nx[1],
            y0: log ? Math.max(ny[0], 1e-12) : Math.max(ny[0], 0),
            y1: ny[1]
        };
        // Zoomed all the way back out is the same as fitted.
        if (factor > 1 && this.atOrBeyondFit()) {
            this.view = null;
        }
        this.render();
    };

    /** True once zooming out has reached the fitted view. */
    Chart.prototype.atOrBeyondFit = function () {
        if (!this.view) { return true; }
        var d = this.dataBounds();
        return this.view.x1 >= d.x1 && this.view.y1 >= d.y1;
    };

    Chart.prototype.reset = function () {
        this.view = null;
        this.render();
    };

    // ------------------------------------------------------------- controls

    function renderAll() {
        charts.forEach(function (c) { c.render(); });
    }

    function setUp() {
        data = JSON.parse(document.getElementById('sb-data').textContent);
        applyColors();

        document.querySelectorAll('[data-chart]').forEach(function (box) {
            var id = box.getAttribute('data-chart');
            var series = data.series[id];
            charts.push(new Chart({
                id: id,
                sizes: series.sizes,
                values: series.values,
                fitted: series.fitted,
                yLabel: series.label,
                svg: box.querySelector('svg'),
                tooltip: box.querySelector('.tooltip'),
                zoomState: document.querySelector('[data-zoom-state="' + id + '"]')
            }));
        });

        // --- scale: a segmented control, so the current mode is visible
        function paintScale() {
            document.querySelectorAll('[data-scale]').forEach(function (btn) {
                var on = (btn.getAttribute('data-scale') === 'log') === prefs.logScale;
                btn.setAttribute('aria-pressed', String(on));
            });
        }
        document.querySelectorAll('[data-scale]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var wantLog = btn.getAttribute('data-scale') === 'log';
                if (wantLog === prefs.logScale) { return; }
                prefs.logScale = wantLog;
                paintScale();
                savePrefs();
                // The old window means nothing on the other scale.
                charts.forEach(function (c) { c.view = null; });
                renderAll();
            });
        });
        paintScale();

        // --- per-chart zoom buttons
        document.querySelectorAll('[data-zoom]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var chart = charts.find(function (c) {
                    return c.spec.id === btn.getAttribute('data-zoom');
                });
                if (!chart) { return; }
                var act = btn.getAttribute('data-act');
                if (act === 'fit') { chart.reset(); }
                else if (act === 'in') { chart.zoomAt(1 / 1.3); }
                else { chart.zoomAt(1.3); }
            });
        });

        function syncPickers() {
            ['measured', 'fitted'].forEach(function (role) {
                document.getElementById('sb-color-' + role).value = activeColor(role);
            });
        }

        ['measured', 'fitted'].forEach(function (role) {
            var input = document.getElementById('sb-color-' + role);
            input.value = activeColor(role);
            input.addEventListener('input', function () {
                prefs[role] = input.value;
                applyColors();
                savePrefs();
                if (host.saveColor) { host.saveColor(role, input.value); }
            });
        });

        document.getElementById('sb-reset-colors').addEventListener('click', function () {
            prefs.measured = '';
            prefs.fitted = '';
            applyColors();
            savePrefs();
            syncPickers();
            if (host.saveColor) {
                host.saveColor('measured', '');
                host.saveColor('fitted', '');
            }
        });

        // --- theme (preview only; inside VS Code the editor decides)
        function paintTheme() {
            document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
                var on = (btn.getAttribute('data-theme-set') === 'dark') === isDark();
                btn.setAttribute('aria-pressed', String(on));
            });
        }
        document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                document.body.dataset.theme = btn.getAttribute('data-theme-set');
                paintTheme();
                syncPickers();
                renderAll();
            });
        });
        paintTheme();

        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
            syncPickers();
            renderAll();
        });

        renderAll();
    }

    // Exposed so a check can compare this fit against _best_fit in
    // python/common/complexity.py. Nothing in the page reads it.
    window.sbInternals = {
        MODELS: MODELS,
        DEFAULTS: DEFAULTS,
        fitScale: fitScale,
        classesToDraw: classesToDraw,
        niceTicks: niceTicks,
        logTicks: logTicks,
        decimalsFor: decimalsFor,
        fmt: fmt,
        shortNum: shortNum
    };

    if (typeof document === 'undefined') {
        return;                              // loaded by the Node check
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setUp);
    } else {
        setUp();
    }
})();
