#!/usr/bin/env pwsh
# Interactive setup (Windows / pwsh). Everything it creates lands in .\.pst and
# .\.venv and is reversible via .\teardown.ps1 — it never touches your global
# VS Code install.
Set-Location $PSScriptRoot
$ExtDir = Join-Path $PSScriptRoot ".pst\extensions"

function Banner {
    Write-Host ''
    Write-Host ' ___   ___   _    __   __ ___     ___  ___  _  _   ___  _  _ ' -ForegroundColor Yellow
    Write-Host '/ __| / _ \ | |   \ \ / /| __|   | _ )| __|| \| | / __|| || |' -ForegroundColor DarkYellow
    Write-Host '\__ \| (_) || |__  \ V / | _|    | _ \| _| | .` || (__ | __ |' -ForegroundColor Red
    Write-Host '|___/ \___/ |____|  \_/  |___|   |___/|___||_|\_| \___||_||_|' -ForegroundColor DarkRed
    Write-Host "  one environment for every judge" -ForegroundColor DarkGray
    Write-Host "  self-contained: everything lands in .\.pst and .\.venv`n" -ForegroundColor DarkGray
}
function Step($m) { Write-Host "`n==> $m" -ForegroundColor Blue }
function Ok($m)   { Write-Host "    [ok] $m" -ForegroundColor Green }
function Info($m) { Write-Host "    $m" -ForegroundColor DarkGray }
function Skip($m) { Write-Host "    --   $m" -ForegroundColor DarkGray }
function Warn($m) { Write-Host "    !    $m" -ForegroundColor Yellow }
function Ask($q, $def = 'Y') {
    $hint = if ($def -eq 'Y') { '[Y/n]' } else { '[y/N]' }
    $ans = Read-Host "? $q $hint"
    if ([string]::IsNullOrWhiteSpace($ans)) { $ans = $def }
    return $ans -match '^[Yy]'
}

Banner

# 1) VS Code extensions (repo-local, no global footprint) --------------------
$exts = @('ms-python.python', 'ms-python.debugpy', 'ms-vscode.cpptools', 'redhat.java', 'vscjava.vscode-java-debug', 'cweijan.vscode-office')
Step "VS Code extensions ($($exts.Count) recommended: Python, C/C++, Java debug)"
if (Get-Command code -ErrorAction SilentlyContinue) {
    if (Ask "Install them into the repo (.\.pst\extensions, not global)?" 'Y') {
        New-Item -ItemType Directory -Force -Path $ExtDir | Out-Null
        $codeArgs = @('--extensions-dir', $ExtDir)
        foreach ($e in $exts) { $codeArgs += @('--install-extension', $e) }
        code @codeArgs --force 2>&1 | Out-Null
        $installed = (code --extensions-dir $ExtDir --list-extensions 2>$null) -join "`n"
        foreach ($e in $exts) {
            if ($installed -match [regex]::Escape($e)) { Ok $e } else { Warn "failed: $e" }
        }
        Info "these live only in .\.pst - open the repo with them via: .\code.ps1"
    } else { Skip "skipped - listed in .vscode/extensions.json for the workspace prompt" }
} else {
    Warn "'code' CLI not found - accept the recommended-extensions prompt in VS Code, then re-run."
}

# 2) Python dev deps (in a repo-local venv) ----------------------------------
Step "Python dev dependencies (optional)"
if (Get-Command python -ErrorAction SilentlyContinue) {
    if (Ask "Install pytest into .\.venv? (the runner itself needs nothing)" 'N') {
        if (-not (Test-Path .venv)) { python -m venv .venv }
        & ".venv\Scripts\pip.exe" install -q -r requirements.txt
        if ($LASTEXITCODE -eq 0) { Ok "pytest ready - run: .venv\Scripts\pytest" }
        else { Warn "pip install failed" }
    } else { Skip "skipped pytest" }
} else { Warn "python not on host - fine, .\run.ps1 runs everything in a container" }

# 3) Container image (optional) ----------------------------------------------
Step "Container image (optional)"
if ((Get-Command docker -ErrorAction SilentlyContinue) -or (Get-Command podman -ErrorAction SilentlyContinue)) {
    if (Ask "Build the solvebench image now?" 'N') {
        .\run.ps1 --stats | Out-Null
        if ($LASTEXITCODE -eq 0) { Ok "image ready (remove later with .\teardown.ps1)" } else { Warn "build failed" }
    } else { Skip "skipped - built automatically on first .\run.ps1" }
} else { Skip "no docker/podman - use PST_NATIVE=1 with local tools" }

Step "Toolchain check"
foreach ($t in @('python', 'g++', 'javac', 'java', 'docker')) {
    if (Get-Command $t -ErrorAction SilentlyContinue) { Ok $t } else { Skip "$t (optional)" }
}
Write-Host "`nSetup complete! Everything is under .\.pst and .\.venv." -ForegroundColor Green
Write-Host "  Run:    .\run.ps1 --stats"
Write-Host "  Edit:   .\code.ps1   (VS Code scoped to this repo)"
Write-Host "  Remove: .\teardown.ps1`n"
