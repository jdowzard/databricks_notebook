@echo off
REM Databricks Notebook Runner - Windows Batch Wrapper
REM This wrapper calls the PowerShell script with proper execution policy

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Call PowerShell script with bypass execution policy
powershell.exe -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run-notebook.ps1" %*

REM Preserve exit code
exit /b %ERRORLEVEL%
