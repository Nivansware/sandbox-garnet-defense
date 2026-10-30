@echo off
title Build Executable .exe - Nivans Gym
echo ====================================================
echo  MEMBANGUN FILE .EXE DENGAN PYINSTALLER
echo  Nivans Gym - Sistem Absensi & Manajemen Member
echo ====================================================
echo.

cd /d "%~dp0"

echo [1/3] Memeriksa instalasi PyInstaller...
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Mengunduh dan memasang PyInstaller...
    pip install pyinstaller
)

echo [2/3] Membangun executable standalone (.exe)...
pyinstaller --noconfirm --onedir --windowed --name "NivansGymApp" --collect-all customtkinter main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================
    echo  SUKSES! Aplikasi .exe berhasil dibuat di:
    echo  dist\NivansGymApp\NivansGymApp.exe
    echo ====================================================
) else (
    echo.
    echo Terjadi kendala saat proses build .exe.
)

pause
