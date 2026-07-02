#!/usr/bin/env pwsh
# Remove everything setup.ps1 / code.ps1 created (Windows/pwsh). Repo-local only,
# except the optional 'pst-runner' docker image.
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

Write-Host @"
     ____   ____   _____
    |  _ \ / ___| |_   _|   cleanup
    |  __/  ___) |  | |
    |_|    |____/   |_|
"@ -ForegroundColor Cyan

Step "Repo-local artifacts"
$targets = @('.pst', '.venv', '.pytest_cache', 'report.html')
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
    & $engine image inspect pst-runner *> $null
    if ($LASTEXITCODE -eq 0) {
        if (Ask "Remove the 'pst-runner' image?" 'Y') { & $engine rmi pst-runner *> $null; Ok "removed pst-runner image" }
        else { Skip "kept pst-runner image" }
    } else { Skip "no pst-runner image present" }
} else { Skip "no docker/podman" }

Write-Host "`nTeardown complete. Tracked repo files are untouched.`n" -ForegroundColor Green
