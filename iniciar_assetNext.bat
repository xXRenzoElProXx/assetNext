@echo off
setlocal enabledelayedexpansion

echo ================================
echo  Activando entorno virtual...
echo ================================
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
) else (
    echo ❌ Error: No se encontró el entorno virtual. ¿Ejecutaste python -m venv venv?
    pause
    exit /b
)

echo.
echo ================================
echo  Verificando archivo requirements.txt...
echo ================================

REM Verificar si existe requirements.txt
if not exist requirements.txt (
    echo ⚠️  requirements.txt no encontrado. Creando archivo vacío...
    echo. > requirements.txt
)

REM Calcular hash actual
for /f %%i in ('certutil -hashfile requirements.txt SHA256 ^| find /v "hash" ^| find /v ":"') do set "currentHash=%%i"

REM Leer hash previo
set "hashFile=.last_requirements_hash"
set "prevHash="
if exist %hashFile% (
    set /p prevHash=<%hashFile%
)

REM Comparar hashes
if "!currentHash!"=="!prevHash!" (
    echo ✅ No hay cambios en requirements.txt. Saltando pip install...
) else (
    echo 🔄 Cambios detectados. Instalando dependencias...
    pip install -r requirements.txt
    echo !currentHash! > %hashFile%
)

echo.
echo ================================
echo  Iniciando servidor Flask
echo ================================
python run.py

pause
