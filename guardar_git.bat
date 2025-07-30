@echo off
setlocal enabledelayedexpansion

REM Obtener fecha y hora con formato YYYY-MM-DD HH:MM:SS
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set dia=%%a
    set mes=%%b
    set anio=%%c
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set hora=%%a
    set min=%%b
)

REM Ajustar formato de hora para 24h si usa AM/PM
set "AMPM="
echo %time% | find /i "PM" >nul && set AMPM=PM
echo %time% | find /i "AM" >nul && set AMPM=AM
if "%AMPM%"=="PM" (
    if %hora% LSS 12 (
        set /a hora=1%hora%-100+12
    )
) else (
    if "%AMPM%"=="AM" (
        if "%hora%"=="12" (
            set hora=00
        )
    )
)

REM Formato final
set commitMsg=%anio%-%mes%-%dia% %hora%:%min%:%time:~6,2%

echo ================================
echo  Guardando en Git...
echo ================================

git add .
git commit -m "%commitMsg%"
git push origin main

echo.
echo ✅ Cambios subidos con mensaje: %commitMsg%
pause
