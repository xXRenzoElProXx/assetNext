@echo off
echo Activando entorno virtual...
call venv\Scripts\activate

echo Iniciando servidor Flask en modo desarrollo...
python run.py

pause
