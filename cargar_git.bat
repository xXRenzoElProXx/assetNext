@echo off
echo ================================
echo  Cargando últimos cambios desde Git...
echo ================================
git pull origin main

echo.
echo ================================
echo  Ejecutando iniciar_assetNext.bat...
echo ================================
call iniciar_assetNext.bat

pause
