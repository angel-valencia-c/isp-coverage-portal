#!/bin/bash

# Script de verificación de la Fase 1
# Este script verifica que todos los componentes de la Fase 1 estén correctamente configurados

echo "=========================================="
echo "VERIFICACIÓN DE FASE 1"
echo "Portal de Verificación de Cobertura"
echo "Internet Regional"
echo "=========================================="
echo ""

# Verificar Python 3.12
echo "1. Verificando Python..."
if command -v python3.12 &> /dev/null; then
    echo "   ✅ Python 3.12 encontrado"
    python3.12 --version
elif command -v python3 &> /dev/null; then
    echo "   ⚠️  Python 3 encontrado (se recomienda 3.12)"
    python3 --version
else
    echo "   ❌ Python no encontrado"
fi
echo ""

# Verificar estructura de carpetas
echo "2. Verificando estructura de carpetas..."
carpetas=(
    "app"
    "app/models"
    "app/routes"
    "app/services"
    "app/utils"
    "tests"
    "public/css"
    "public/js"
    "public/images"
)

for carpeta in "${carpetas[@]}"; do
    if [ -d "$carpeta" ]; then
        echo "   ✅ $carpeta"
    else
        echo "   ❌ $carpeta (FALTA)"
    fi
done
echo ""

# Verificar archivos principales
echo "3. Verificando archivos principales..."
archivos=(
    "requirements.txt"
    ".env.example"
    ".gitignore"
    "pytest.ini"
    "README.md"
    "app/__init__.py"
    "app/config.py"
    "app/extensions.py"
    "app/routes/health.py"
    "tests/conftest.py"
    "tests/test_health.py"
)

for archivo in "${archivos[@]}"; do
    if [ -f "$archivo" ]; then
        echo "   ✅ $archivo"
    else
        echo "   ❌ $archivo (FALTA)"
    fi
done
echo ""

# Verificar entorno virtual
echo "4. Verificando entorno virtual..."
if [ -d "venv" ]; then
    echo "   ✅ Entorno virtual encontrado"
    if [ -f "venv/bin/activate" ]; then
        echo "   ✅ Script de activación disponible"
    fi
else
    echo "   ⚠️  Entorno virtual no encontrado"
    echo "   💡 Crear con: python3.12 -m venv venv"
fi
echo ""

# Verificar dependencias instaladas
echo "5. Verificando dependencias..."
if [ -f "venv/bin/pip" ]; then
    echo "   Verificando paquetes instalados..."
    source venv/bin/activate
    if pip show flask &> /dev/null; then
        echo "   ✅ Flask instalado"
    else
        echo "   ❌ Flask no instalado"
    fi
    
    if pip show flask-sqlalchemy &> /dev/null; then
        echo "   ✅ Flask-SQLAlchemy instalado"
    else
        echo "   ❌ Flask-SQLAlchemy no instalado"
    fi
    
    if pip show pytest &> /dev/null; then
        echo "   ✅ pytest instalado"
    else
        echo "   ❌ pytest no instalado"
    fi
    deactivate
else
    echo "   ⚠️  No se puede verificar (entorno virtual no activado)"
fi
echo ""

# Verificar archivo .env
echo "6. Verificando configuración de entorno..."
if [ -f ".env" ]; then
    echo "   ✅ Archivo .env encontrado"
else
    echo "   ⚠️  Archivo .env no encontrado"
    echo "   💡 Crear con: cp .env.example .env"
fi
echo ""

# Resumen
echo "=========================================="
echo "RESUMEN"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Crear entorno virtual: python3.12 -m venv venv"
echo "2. Activar entorno: source venv/bin/activate"
echo "3. Instalar dependencias: pip install -r requirements.txt"
echo "4. Configurar .env: cp .env.example .env"
echo "5. Crear base de datos MySQL"
echo "6. Inicializar migraciones: flask db init"
echo "7. Ejecutar servidor: flask run"
echo ""
echo "=========================================="
