@echo off
REM Windows cmd shim -> PowerShell wrapper. Prefers pwsh (PowerShell 7),
REM falls back to built-in Windows PowerShell.
where pwsh >nul 2>nul
if %errorlevel%==0 (
  pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
) else (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
)
exit /b %errorlevel%
