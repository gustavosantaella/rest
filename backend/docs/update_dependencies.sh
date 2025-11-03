#!/bin/bash

echo "===================================="
echo "Actualizando dependencias..."
echo "===================================="
echo ""

echo "Desinstalando versiones antiguas..."
pip uninstall -y passlib bcrypt

echo ""
echo "Instalando versiones compatibles..."
pip install passlib==1.7.4
pip install bcrypt==4.0.1

echo ""
echo "===================================="
echo "Actualización completada!"
echo "===================================="
echo ""
echo "Ahora puedes ejecutar: python run.py"

