#!/usr/bin/env pwsh
# Interactive one-time setup for Problem Solving Training (Windows / pwsh).
Set-Location $PSScriptRoot

function Banner {
    Write-Host @"
     ____   ____   _____
    |  _ \ / ___| |_   _|
    | |_) |\___ \   | |
    |  __/  ___) |  | |
    |_|    |____/   |_|
"@ -ForegroundColor Cyan
    Write-Host "    Problem · Solving · Training" -ForegroundColor White
    Write-Host "    polyglot practice - python | c++ | java`n" -ForegroundColor DarkGray
}
function Step($m) { Write-Host "`n==> $m" -ForegroundColor Blue }
function Ok($m)   { Write-Host "    [ok] $m" -ForegroundColor Green }
function Skip($m) { Write-Host "    --   $m" -ForegroundColor DarkGray }
function Warn($m) { Write-Host "    !    $m" -ForegroundColor Yellow }
function Ask($q, $def = 'Y') {
    $hint = if ($def -eq 'Y') { '[Y/n]' } else { '[y/N]' }
    $ans = Read-Host "? $q $hint"
    if ([string]::IsNullOrWhiteSpace($ans)) { $ans = $def }
    return $ans -match '^[Yy]'
}

Banner

$exts = @('ms-python.python', 'ms-python.debugpy', 'ms-vscode.cpptools', 'redhat.java', 'vscjava.vscode-java-debug')
Step "VS Code extensions ($($exts.Count) recommended: Python, C/C++, Java debug)"
if (Get-Command code -ErrorAction SilentlyContinue) {
    if (Ask "Install them now?" 'Y') {
        foreach ($e in $exts) { code --install-extension $e --force | Out-Null; Ok $e }
    } else { Skip "skipped - listed in .vscode/extensions.json for later" }
} else {
    Warn "'code' CLI not found - accept the recommended-extensions prompt in VS Code, then re-run."
}

Step "Python dev dependencies (optional)"
if (Get-Command python -ErrorAction SilentlyContinue) {
    if (Ask "Install pytest? (the runner itself needs nothing)" 'N') {
        python -m pip install -r requirements.txt; Ok "pytest installed"
    } else { Skip "skipped pytest" }
} else { Warn "python not on host - fine, .\run.ps1 runs everything in a container" }

Step "Toolchain check"
foreach ($t in @('python', 'g++', 'javac', 'java', 'docker')) {
    if (Get-Command $t -ErrorAction SilentlyContinue) { Ok $t } else { Skip "$t (optional)" }
}
Write-Host "`nSetup complete!  Next: .\run.ps1 --stats`n" -ForegroundColor Green
