@echo off
rem Checks the scripts
rem Copyright (C) 2024 kaoru  <https://www.tetengo.org/>

setlocal
if "%1" == "" (
    set BASEDIR=%~dp0
) else (
    set BASEDIR=%1
)

echo Checking %BASEDIR%...
mypy --strict --no-warn-unused-ignores %BASEDIR%
if errorlevel 1 exit /b 1
black --quiet %BASEDIR%
if errorlevel 1 exit /b 1
for %%f in (%BASEDIR%%\*.py) do (
    isort --profile black %%f
    if errorlevel 1 exit /b 1
)
