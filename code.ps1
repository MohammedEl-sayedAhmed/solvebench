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
# Safe ONLY because this launcher refuses to open anything outside this repo.
$settings = Join-Path $dataDir "User\settings.json"
if (-not (Test-Path $settings)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $settings) | Out-Null
    '{ "security.workspace.trust.enabled": false }' | Set-Content $settings
}

# Seed repo-local keybindings once (the .pst profile is git-ignored, so these
# can't be committed): duplicate the current line up/down with Ctrl+Alt+Up/Down.
# A user keybinding overrides the built-in default on those keys.
$keybindings = Join-Path $dataDir "User\keybindings.json"
if (-not (Test-Path $keybindings)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $keybindings) | Out-Null
    @'
// Repo-scoped keybindings for the .\code.ps1 editor (--user-data-dir .pst).
// Seeded by code.sh / code.ps1 if missing; safe to edit.
[
  {
    "key": "ctrl+alt+up",
    "command": "editor.action.copyLinesUpAction",
    "when": "editorTextFocus && !editorReadonly"
  },
  {
    "key": "ctrl+alt+down",
    "command": "editor.action.copyLinesDownAction",
    "when": "editorTextFocus && !editorReadonly"
  }
]
'@ | Set-Content $keybindings
}

# Guard: since the .pst profile skips the trust prompt, only paths INSIDE this
# repo may be opened with it. Use your normal VS Code for anything else.
$sep = [IO.Path]::DirectorySeparatorChar
foreach ($a in $args) {
    if ($a -like '-*') { continue }                      # skip CLI flags
    $p = $a -replace ':\d+(:\d+)?$', ''                  # tolerate --goto file:line
    $abs = [IO.Path]::GetFullPath((Join-Path (Get-Location) $p))
    if (-not ($abs -eq $PSScriptRoot -or $abs.StartsWith("$PSScriptRoot$sep"))) {
        Write-Error "code.ps1 only opens paths inside this repo (the .pst profile skips the trust prompt). Refusing: $a"
        exit 1
    }
}

$target = if ($args.Count -gt 0) { $args } else { @('.') }
code --extensions-dir $extDir --user-data-dir $dataDir @target
