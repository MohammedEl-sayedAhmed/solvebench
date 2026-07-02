#!/usr/bin/env pwsh
# init.ps1 — after forking, reset the repo to a clean slate for YOU (Windows).
# Removes example solutions + inputs, resets the README index, writes your
# platform handles, and (optionally) starts fresh git history. Keeps tooling.
Set-Location $PSScriptRoot

function Step($m) { Write-Host "`n==> $m" -ForegroundColor Blue }
function Ok($m)   { Write-Host "    [ok] $m" -ForegroundColor Green }
function Skip($m) { Write-Host "    --   $m" -ForegroundColor DarkGray }
function Warn($m) { Write-Host "    !    $m" -ForegroundColor Yellow }
function Ask($q, $def = 'Y') {
    $hint = if ($def -eq 'Y') { '[Y/n]' } else { '[y/N]' }
    $a = Read-Host "? $q $hint"
    if ([string]::IsNullOrWhiteSpace($a)) { $a = $def }
    return $a -match '^[Yy]'
}

Write-Host @"
     ____   ____   _____    init
    |  _ \ / ___| |_   _|
    |  __/  ___) |  | |
    |_|    |____/   |_|
"@ -ForegroundColor Cyan

Warn "This clears ALL solutions and puzzle inputs and resets the README index."
if (-not (Ask "Continue?" 'N')) { Write-Host "    aborted - nothing changed"; exit 0 }

Step "Clearing example solutions and inputs"
foreach ($lang in 'python', 'cpp', 'java') {
    if (Test-Path $lang) {
        Get-ChildItem $lang -Directory | Where-Object { $_.Name -ne 'common' } | Remove-Item -Recurse -Force
    }
}
if (Test-Path inputs) { Get-ChildItem inputs | Remove-Item -Recurse -Force }
Ok "removed solutions (kept common/ + templates/) and puzzle inputs"

Step "Your profile (leave blank to skip a platform)"
$name = Read-Host "? Your name"
$gh = Read-Host "? GitHub username"
$lc = Read-Host "? LeetCode username"
$cw = Read-Host "? Codewars username"
$hr = Read-Host "? HackerRank username"
$cf = Read-Host "? Codeforces username"
[ordered]@{ name = $name; github = $gh; leetcode = $lc; codewars = $cw; hackerrank = $hr; codeforces = $cf } |
    ConvertTo-Json | Set-Content profile.json
python scripts/apply_profile.py | Out-Null; Ok "wrote profile.json and updated the README profile"
python scripts/reset_index.py | Out-Null; Ok "README solutions index cleared"

Step "Git history"
if (Ask "Start fresh git history? (removes ALL past commits)" 'N') {
    Remove-Item -Recurse -Force .git
    git init -q; git add -A; git commit -q -m "Initial commit"; Ok "fresh git history created"
} else { Skip "kept existing git history" }

Write-Host "`nClean slate ready!" -ForegroundColor Green
Write-Host "  Add a solution: .\run.ps1 new leetcode/easy/two_sum --lang py"
Write-Host "  Set up tooling: .\setup.ps1`n"
