#!/usr/bin/env pwsh
# Cross-platform wrapper: Windows PowerShell 5.1, or pwsh on Linux/macOS.
# Mirrors run.sh so the repo runs identically everywhere via a container.
#
#   .\run.ps1                            # run every solution
#   .\run.ps1 leetcode/easy/two_sum      # run one problem, all languages
#   .\run.ps1 --stats                    # inventory grouped by platform
#   .\run.ps1 new leetcode/easy/foo --lang cpp   # scaffold a new solution
#   .\run.ps1 shell                      # open a shell inside the container
#
# Set PST_NATIVE=1 to run on the host toolchain instead of a container.
$ErrorActionPreference = 'Stop'
$Image = 'pst-runner'
Set-Location -Path $PSScriptRoot

$argv = @($args)
$rest = if ($argv.Count -gt 1) { $argv[1..($argv.Count - 1)] } else { @() }

# --- Native escape hatch ----------------------------------------------------
if ($env:PST_NATIVE -eq '1') {
    $py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' }
          elseif (Get-Command python3 -ErrorAction SilentlyContinue) { 'python3' }
          else { 'py' }
    switch ($argv[0]) {
        'new'   { & $py new.py @rest }
        'shell' { & $py }
        default { & $py run.py @argv }
    }
    exit $LASTEXITCODE
}

# --- Pick a container engine ------------------------------------------------
$engine = if (Get-Command docker -ErrorAction SilentlyContinue) { 'docker' }
          elseif (Get-Command podman -ErrorAction SilentlyContinue) { 'podman' }
          else { $null }
if (-not $engine) {
    Write-Error "Neither docker nor podman is installed. Install one, or set PST_NATIVE=1 to run on the host toolchain."
    exit 1
}

# --- Build the image on first use -------------------------------------------
& $engine image inspect $Image *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host ">> Building $Image image (first run only)..."
    & $engine build -t $Image .
}

# On Linux/macOS keep host file ownership; on Windows Docker Desktop handles it.
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
    'new'   { Invoke-Engine (@('python3', 'new.py') + $rest) }
    'shell' { Invoke-Engine @('bash') }
    default { Invoke-Engine (@('python3', 'run.py') + $argv) }
}
exit $LASTEXITCODE
