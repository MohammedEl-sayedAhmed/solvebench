#!/usr/bin/env pwsh
# Cross-platform wrapper: Windows PowerShell 5.1, or pwsh on Linux/macOS.
# Uses a container on the host; runs natively automatically inside the Dev
# Container (or any container) and when no container engine is available.
#
#   .\run.ps1                            # run every solution
#   .\run.ps1 leetcode/easy/two_sum      # run one problem, all languages
#   .\run.ps1 --stats                    # inventory grouped by platform
#   .\run.ps1 new <url|path> --lang cpp  # scaffold a new solution
#   .\run.ps1 complexity <problem>       # estimate a solution's Big-O
#   .\run.ps1 shell                      # open a shell inside the container
#
# Force native execution with PST_NATIVE=1.
$ErrorActionPreference = 'Stop'
$Image = 'pst-runner'
Set-Location -Path $PSScriptRoot

$argv = @($args)
$rest = if ($argv.Count -gt 1) { $argv[1..($argv.Count - 1)] } else { @() }

function Invoke-Native {
    $py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' }
          elseif (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' }
          else { 'py' }
    switch ($argv[0]) {
        'new'        { & $py new.py @rest }
        'complexity' { & $py complexity.py @rest }
        'shell'      { & $py }
        default      { & $py run.py @argv }
    }
    exit $LASTEXITCODE
}

# Native path: asked for it, or already inside the toolchain container.
if ($env:PST_NATIVE -eq '1' -or $env:PST_IN_CONTAINER -eq '1' -or (Test-Path '/.dockerenv')) {
    Invoke-Native
}

# Otherwise pick a container engine; if none, fall back to native (don't error).
$engine = if (Get-Command docker -ErrorAction SilentlyContinue) { 'docker' }
          elseif (Get-Command podman -ErrorAction SilentlyContinue) { 'podman' }
          else { $null }
if (-not $engine) {
    Write-Host "note: no docker/podman found — running on the local toolchain."
    Invoke-Native
}

& $engine image inspect $Image *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host ">> Building $Image image (first run only)..."
    & $engine build -t $Image .
}

$userArgs = @()
if (Get-Command id -ErrorAction SilentlyContinue) {
    $userArgs = @('--user', "$(id -u):$(id -g)", '-e', 'HOME=/tmp')
}
$tty = @()
if (-not [Console]::IsOutputRedirected) { $tty = @('-t') }
$mount = "$($PWD.Path):/repo"

function Invoke-Engine {
    param([string[]]$Cmd)
    & $engine run --rm -i @tty @userArgs -v $mount -w /repo $Image @Cmd
}

switch ($argv[0]) {
    'new'        { Invoke-Engine (@('python3', 'new.py') + $rest) }
    'complexity' { Invoke-Engine (@('python3', 'complexity.py') + $rest) }
    'shell'      { Invoke-Engine @('bash') }
    default      { Invoke-Engine (@('python3', 'run.py') + $argv) }
}
exit $LASTEXITCODE
