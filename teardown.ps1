#!/usr/bin/env pwsh
# Remove everything setup.ps1 / code.ps1 created (Windows/pwsh). Repo-local only,
# except the optional 'solvebench' docker image.
Set-Location $PSScriptRoot

function Step($m) { Write-Host "`n==> $m" -ForegroundColor Blue }
function Ok($m)   { Write-Host "    [ok] $m" -ForegroundColor Green }
function Skip($m) { Write-Host "    --   $m" -ForegroundColor DarkGray }
function Ask($q, $def = 'Y') {
    $hint = if ($def -eq 'Y') { '[Y/n]' } else { '[y/N]' }
    $ans = Read-Host "? $q $hint"
    if ([string]::IsNullOrWhiteSpace($ans)) { $ans = $def }
    return $ans -match '^[Yy]'
}

    Write-Host ''
    Write-Host '  \      ' -NoNewline -ForegroundColor Red; Write-Host '  ' -NoNewline; Write-Host ' ___   ___   _    __   __ ___     ___  ___  _  _   ___  _  _ ' -ForegroundColor Yellow
    Write-Host '   \     ' -NoNewline -ForegroundColor Red; Write-Host '  ' -NoNewline; Write-Host '/ __| / _ \ | |   \ \ / /| __|   | _ )| __|| \| | / __|| || |' -ForegroundColor DarkYellow
    Write-Host '   /     ' -NoNewline -ForegroundColor Red; Write-Host '  ' -NoNewline; Write-Host '\__ \| (_) || |__  \ V / | _|    | _ \| _| | .` || (__ | __ |' -ForegroundColor Red
    Write-Host '  /   ' -NoNewline -ForegroundColor Red; Write-Host '__ ' -NoNewline -ForegroundColor Yellow; Write-Host '  ' -NoNewline; Write-Host '|___/ \___/ |____|  \_/  |___|   |___/|___||_|\_| \___||_||_|' -ForegroundColor DarkRed
Write-Host "  teardown - remove everything setup created`n" -ForegroundColor DarkGray

Step "Repo-local artifacts"
# The code.ps1 editor profile lives outside the repo (same derivation as
# code.ps1 — it can't sit under .\.pst or the Java language server refuses to
# import the project). Remove it here so teardown still erases every trace.
# Same derivation as code.ps1: LOCALAPPDATA on Windows, ~/.cache elsewhere,
# path lower-cased before hashing (Windows paths are case-insensitive).
$cacheRoot = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME '.cache' }
$pathKey = $PSScriptRoot.ToLowerInvariant()
$md5 = [System.Security.Cryptography.MD5]::Create()
$hash = ([BitConverter]::ToString($md5.ComputeHash([Text.Encoding]::UTF8.GetBytes($pathKey))) -replace '-', '').Substring(0, 8).ToLower()
$profileDir = Join-Path (Join-Path $cacheRoot 'solvebench') "$(Split-Path $pathKey -Leaf)-$hash"
$targets = @('.pst', '.venv', '.pytest_cache', 'report.html', $profileDir)
$present = @($targets | Where-Object { Test-Path $_ })
foreach ($t in $present) { Write-Host "    $t" }
$compiled = @(Get-ChildItem -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -in '__pycache__' -or $_.Extension -in '.pyc', '.class', '.out' })

if ($present.Count -eq 0 -and $compiled.Count -eq 0) {
    Ok "nothing to remove - already clean"
} elseif (Ask "Remove these?" 'Y') {
    foreach ($t in $present) { Remove-Item -Recurse -Force $t; Ok "removed $t" }
    if ($compiled.Count -gt 0) { $compiled | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; Ok "removed caches/build files" }
} else {
    Skip "kept repo-local artifacts"
}

Step "Container image (docker daemon)"
$engine = if (Get-Command docker -ErrorAction SilentlyContinue) { 'docker' }
          elseif (Get-Command podman -ErrorAction SilentlyContinue) { 'podman' }
          else { $null }
if ($engine) {
    & $engine image inspect solvebench *> $null
    if ($LASTEXITCODE -eq 0) {
        if (Ask "Remove the 'solvebench' image?" 'Y') { & $engine rmi solvebench *> $null; Ok "removed solvebench image" }
        else { Skip "kept solvebench image" }
    } else { Skip "no solvebench image present" }
} else { Skip "no docker/podman" }

Write-Host "`nTeardown complete. Tracked repo files are untouched.`n" -ForegroundColor Green
