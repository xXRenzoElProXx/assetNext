@echo off
setlocal enabledelayedexpansion

echo ================================
echo Guardando en Git...
echo ================================

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Git no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si estamos en un repositorio Git
if not exist ".git" (
    echo ❌ Error: No estás en un repositorio Git
    pause
    exit /b 1
)

REM Verificar si hay cambios
git diff --quiet
if not errorlevel 1 (
    git diff --cached --quiet
    if not errorlevel 1 (
        echo ℹ️ No hay cambios para commitear
        pause
        exit /b 0
    )
)

REM Mostrar estado actual
echo Estado actual del repositorio:
git status --short

REM Obtener timestamp mejorado
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set dia=%%a
    set mes=%%b  
    set anio=%%c
)

for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set hora=%%a
    set min=%%b
    set seg=%%c
)

REM Limpiar espacios
set hora=%hora: =0%
set commitMsg=%anio%-%mes%-%dia% %hora%:%min%:%seg%

echo.
echo Agregando archivos...
git add .
if errorlevel 1 (
    echo ❌ Error al agregar archivos
    pause
    exit /b 1
)

echo Creando commit...
git commit -m "%commitMsg%"
if errorlevel 1 (
    echo ❌ Error al crear commit
    pause
    exit /b 1
)

echo Subiendo cambios...
git push origin main
if errorlevel 1 (
    echo ❌ Error al hacer push. Posibles causas:
    echo - Sin permisos en el repositorio
    echo - Conflictos con el remoto
    echo - Problemas de red
    echo.
    echo Intenta: git pull origin main primero
    pause
    exit /b 1
)

echo.
echo ✅ Cambios subidos exitosamente con mensaje: %commitMsg%
pause