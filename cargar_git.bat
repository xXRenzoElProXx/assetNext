@echo off
echo ================================
echo Cargando últimos cambios desde Git...
echo ================================

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Git no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar conexión al remoto
echo Verificando conexión al repositorio remoto...
git remote -v

REM Verificar archivos eliminados manualmente
echo.
echo Verificando archivos faltantes...
for /f "delims=" %%f in ('git ls-files') do (
    if not exist "%%f" (
        echo ⚠️ Archivo faltante detectado: %%f
        set "missing_files=true"
    )
)

if defined missing_files (
    echo.
    set /p "restore_choice=¿Restaurar archivos faltantes? (s/n): "
    if /i "!restore_choice!"=="s" (
        echo Restaurando archivos faltantes...
        git checkout HEAD -- .
        if errorlevel 1 (
            echo ❌ Error al restaurar archivos
        ) else (
            echo ✅ Archivos restaurados
        )
    )
)

REM Hacer pull
echo.
echo Sincronizando con el repositorio remoto...
git pull origin main
if errorlevel 1 (
    echo ❌ Error al hacer pull. Posibles causas:
    echo - Conflictos de merge
    echo - Sin permisos en el repositorio
    echo - Problemas de red
    pause
    exit /b 1
)

echo ✅ Sincronización exitosa

REM Verificar estado final
echo.
echo Estado final del repositorio:
git status --short

echo.
echo ================================
echo Ejecutando iniciar_assetNext.bat...
echo ================================
call iniciar_assetNext.bat
pause