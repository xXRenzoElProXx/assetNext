@echo off
echo ================================
echo Cargando últimos cambios desde Git...
echo ================================

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Git no está instalado o no está en el PATH
    echo Instala Git desde: https://git-scm.com/
    pause
    exit /b 1
)

REM Verificar si estamos en un repositorio Git
if not exist ".git" (
    echo ❌ Error: No estás en un repositorio Git
    echo Ejecuta primero: git clone https://github.com/xXRenzoElProXx/assetNext.git
    pause
    exit /b 1
)

REM Verificar conexión al remoto
echo Verificando conexión al repositorio remoto...
git remote -v
if errorlevel 1 (
    echo ❌ Error: No se puede conectar al repositorio remoto
    pause
    exit /b 1
)

REM Hacer pull con manejo de errores
git pull origin main
if errorlevel 1 (
    echo ❌ Error al hacer pull. Posibles causas:
    echo - Conflictos de merge
    echo - Sin permisos en el repositorio
    echo - Problemas de red
    echo.
    echo Intenta resolver manualmente con:
    echo git status
    echo git merge --abort (si hay conflictos)
    pause
    exit /b 1
)

echo ✅ Pull exitoso
echo.
echo ================================
echo Ejecutando iniciar_assetNext.bat...
echo ================================
call iniciar_assetNext.bat
pause