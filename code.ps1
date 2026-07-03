#!/usr/bin/env pwsh
# Launch VS Code scoped to THIS repo only: repo-local extensions (.\.pst) + a
# dedicated profile under $env:LOCALAPPDATA\solvebench\<repo>-<id>, so it never
# touches your global VS Code. Remove it all with .\teardown.ps1.
# Run .\setup.ps1 first to populate the extensions.
Set-Location $PSScriptRoot

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
    Write-Error "VS Code 'code' CLI not found on PATH."
    exit 1
}

$extDir = Join-Path $PSScriptRoot ".pst\extensions"
# The profile can't live under .\.pst: the Java language server (Eclipse-based)
# refuses to import any project whose folder contains its own workspace
# metadata ("project overlaps the workspace location"), which broke the Java
# Run|Debug CodeLens. teardown.ps1 removes this directory too.
# %LOCALAPPDATA% on Windows; ~/.cache on pwsh for Linux/macOS (LOCALAPPDATA is
# unset there — without the fallback the profile silently landed back inside
# the repo, resurrecting the very overlap bug this change fixes).
$cacheRoot = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME '.cache' }
# Lower-case the path before hashing: Windows paths are case-insensitive and
# $PSScriptRoot keeps whatever casing the launch used.
$pathKey = $PSScriptRoot.ToLowerInvariant()
$md5 = [System.Security.Cryptography.MD5]::Create()
$hash = ([BitConverter]::ToString($md5.ComputeHash([Text.Encoding]::UTF8.GetBytes($pathKey))) -replace '-', '').Substring(0, 8).ToLower()
$repoId = "$(Split-Path $pathKey -Leaf)-$hash"
$dataDir = Join-Path (Join-Path (Join-Path $cacheRoot 'solvebench') $repoId) 'user-data'

# Seed the repo-local profile's user settings once: a fresh profile starts in
# Restricted Mode, which stops the Java language server from importing projects.
# Safe ONLY because this launcher refuses to open anything outside this repo.
$settings = Join-Path $dataDir "User\settings.json"
if (-not (Test-Path $settings)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $settings) | Out-Null
    '{ "security.workspace.trust.enabled": false }' | Set-Content $settings
}

# Seed the profile's keybindings once (the profile lives outside git, so these
# can't be committed): duplicate the current line up/down with Ctrl+Alt+Up/Down.
# A user keybinding overrides the built-in default on those keys.
$keybindings = Join-Path $dataDir "User\keybindings.json"
if (-not (Test-Path $keybindings)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $keybindings) | Out-Null
    @'
// Keybindings for the repo-scoped editor launched by .\code.ps1.
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
