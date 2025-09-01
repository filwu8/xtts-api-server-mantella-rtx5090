@echo off
chcp 65001 > nul
title Build XTTS API Server Executable

echo ========================================
echo   Build XTTS API Server Executable
echo ========================================
echo.

echo Checking environment...

REM Check virtual environment
if exist ".venv\Scripts\python.exe" (
    echo Found virtual environment
    set PYTHON_EXE=.venv\Scripts\python.exe
    set PIP_EXE=.venv\Scripts\pip.exe
) else (
    echo Virtual environment not found, using system Python
    set PYTHON_EXE=python
    set PIP_EXE=pip
)

echo.
echo Installing PyInstaller...
%PIP_EXE% install pyinstaller

echo.
echo Building executable...

REM 使用PyInstaller构建
%PYTHON_EXE% -m PyInstaller ^
    --onefile ^
    --console ^
    --name "xtts-api-server-mantella" ^
    --add-data "config.ini;." ^
    --hidden-import uvicorn ^
    --hidden-import fastapi ^
    --hidden-import TTS ^
    --hidden-import torch ^
    --hidden-import torchaudio ^
    --hidden-import loguru ^
    --hidden-import pydantic ^
    --clean ^
    xtts_launcher.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful!

    REM Check output file
    if exist "dist\xtts-api-server-mantella.exe" (
        echo Executable location: dist\xtts-api-server-mantella.exe

        REM Move to root directory
        if exist "xtts-api-server-mantella.exe" del "xtts-api-server-mantella.exe"
        move "dist\xtts-api-server-mantella.exe" "xtts-api-server-mantella.exe"
        echo File moved to root directory
    ) else (
        echo Output file not found
    )
) else (
    echo Build failed
)

echo.
echo Cleaning temporary files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "xtts-api-server-mantella.spec" del "xtts-api-server-mantella.spec"

echo.
echo Build completed!
echo.
pause
