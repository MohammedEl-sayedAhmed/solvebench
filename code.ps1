#!/usr/bin/env pwsh
# Launch VS Code scoped to THIS repo only: repo-local extensions + profile under
# .\.pst, so it never touches your global VS Code. Run .\setup.ps1 first.
Set-Location $PSScriptRoot

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
    Write-Error "VS Code 'code' CLI not found on PATH."
    exit 1
}

$extDir = Join-Path $PSScriptRoot ".pst\extensions"
$dataDir = Join-Path $PSScriptRoot ".pst\user-data"

# Seed the repo-local profile's user settings once: a fresh profile starts in
# Restricted Mode, which stops the Java language server from importing projects.
$settings = Join-Path $dataDir "User\settings.json"
if (-not (Test-Path $settings)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $settings) | Out-Null
    '{ "security.workspace.trust.enabled": false }' | Set-Content $settings
}

$target = if ($args.Count -gt 0) { $args } else { @('.') }
code --extensions-dir $extDir --user-data-dir $dataDir @target
