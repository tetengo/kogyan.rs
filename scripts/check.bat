rem @echo off
rem Checks the scripts
rem Copyright (C) 2024 kaoru  <https://www.tetengo.org/>

setlocal
if "%1" == "" (
    set BASEDIR=%~dp0
) else (
    set BASEDIR=%1
)

for %%f in (%BASEDIR%%\*.py) do (
    echo Checking %%~nxf...
    mypy %%f
    if errorlevel 1 exit /b 1
    black %%f
    if errorlevel 1 exit /b 1
    isort --profile black %%f
    if errorlevel 1 exit /b 1
)
