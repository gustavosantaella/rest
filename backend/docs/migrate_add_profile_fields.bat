@echo off
echo ====================================
echo Migracion de Base de Datos
echo ====================================
echo.

.venv\Scripts\python.exe migrate_add_profile_fields.py

echo.
pause

