@echo off
:: Pindah ke folder root proyek
cd %~dp0

:: Informasi awal
echo =====================================================
echo Menyiapkan lingkungan untuk Backend dan Frontend...
echo =====================================================

:: Langkah 1: Membuat dan menginstal dependencies Python
echo [1/4] Memeriksa dan menginstal library Python...
if not exist "venv" (
    echo Virtual environment tidak ditemukan, membuat virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Gagal membuat virtual environment. Pastikan Python terinstal dan PATH sudah benar.
        pause
        exit /b
    )
)
pause
echo Mengaktifkan virtual environment...
call venv\Scripts\activate
pause
echo Menginstal library Python dari requirements.txt...
pip install -r src/requirements.txt || (
    echo Gagal menginstal dependencies Python. Periksa file requirements.txt.
    pause
    exit /b
)
pause
deactivate

:: Langkah 2: Memeriksa dan menginstal dependencies Node.js
echo [2/4] Memeriksa dan menginstal library Node.js untuk React...
cd react-app
pause
if not exist "node_modules" (
    echo Folder node_modules tidak ditemukan, menginstal dependencies...
    npm install || (
        echo Gagal menginstal dependencies Node.js. Periksa file package.json.
        pause
        exit /b
    )
)
pause
