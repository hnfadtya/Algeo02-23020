@echo off
:: Pindah ke folder root proyek (tempat file batch dijalankan)
cd %~dp0

:: Menjalankan aplikasi Python
start cmd /k "python src/react-app/src/app.py"

:: Menjalankan npm run dev
start cmd /k "cd src/react-app && npm run dev"
