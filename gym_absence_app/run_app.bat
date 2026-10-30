@echo off
title Menjalankan Nivans Gym Absence App
echo Membuka aplikasi Nivans Gym...
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Gagal menjalankan aplikasi secara langsung. Mencoba memeriksa dependencies...
    pip install customtkinter
    python main.py
    pause
)
