# Portal de Verificación de Cobertura y Solicitud de Instalación

## Enlaces Costa Grande

Portal web que permite a prospectos verificar disponibilidad de cobertura de internet, consultar planes disponibles, obtener cotización estimada y solicitar instalación.

---

## 🚀 Stack Tecnológico

- **Backend**: Python 3.12 + Flask 3.0.0
- **Base de Datos**: MySQL
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **Migraciones**: Alembic + Flask-Migrate
- **Testing**: pytest + pytest-cov
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla

---

## 📋 Requisitos Previos

- Python 3.12 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)
- Git

---

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd estadia
```

### 2. Crear entorno virtual de Python

```bash
# Linux/Mac
python3.12 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales locales
nano .env  # o tu editor preferido
```

**Variables importantes a configurar:**
- `SECRET_KEY`: Clave secreta para Flask (genera una aleatoria)
- `DATABASE_URL`: URL de conexión a MySQL
- `TESTING_DATABASE_URL`: URL de conexión a BD de testing

### 5. Crear base de datos en MySQL

```sql
CREATE DATABASE enlaces_costa_grande CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE enlaces_costa_grande_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Inicializar migraciones

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🏃 Ejecución

### Servidor de desarrollo

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Configurar variables de Flask
export FLASK_APP=app
export FLASK_ENV=development

# Ejecutar servidor
flask run --host=0.0.0.0 --port=5000
```

El servidor estará disponible en: `http://localhost:5000`

### Endpoints disponibles

- `GET /` - Información de la aplicación
- `GET /health` - Verificación de salud

---

## 🧪 Testing

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con reporte de coverage

```bash
pytest --cov=app --cov-report=html
```

El reporte de coverage se generará en `htmlcov/`. Para verlo:

```bash
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Ejecutar tests específicos

```bash
# Tests de health endpoint
pytest tests/test_health.py

# Tests con verbose
pytest -v

# Tests sin coverage
pytest --no-cov
```

---

## 📁 Estructura del Proyecto

```
estadia/
├── app/                          # Aplicación Flask principal
│   ├── __init__.py              # Factory pattern (create_app)
│   ├── config.py                # Configuración por entorno
│   ├── extensions.py            # Extensiones Flask (db, migrate, cors)
│   ├── models/                  # Modelos SQLAlchemy
│   ├── routes/                  # Blueprints Flask
│   │   └── health.py           # Endpoint de salud
│   ├── services/                # Lógica de negocio
│   └── utils/                   # Utilidades auxiliares
├── migrations/                   # Migraciones Alembic
├── tests/                        # Tests pytest
│   ├── conftest.py              # Fixtures globales
│   └── test_health.py           # Tests de salud
├── public/                       # Frontend estático
│   ├── css/
│   ├── js/
│   └── images/
├── .env.example                  # Template de variables de entorno
├── .gitignore
├── requirements.txt              # Dependencias Python
├── pytest.ini                    # Configuración pytest
└── README.md                     # Este archivo
```

---

## 🗄️ Base de Datos

### Crear migración

```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar migración

```bash
flask db upgrade
```

### Revertir migración

```bash
flask db downgrade
```

### Ver historial de migraciones

```bash
flask db history
```

---

## 🔐 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `FLASK_APP` | Nombre de la aplicación | `app` |
| `FLASK_ENV` | Entorno de ejecución | `development` |
| `SECRET_KEY` | Clave secreta de Flask | `mi-clave-secreta` |
| `DATABASE_URL` | URL de conexión a BD | `mysql+pymysql://user:pass@localhost:3306/db` |
| `TESTING_DATABASE_URL` | URL de BD de testing | `mysql+pymysql://user:pass@localhost:3306/db_test` |
| `LOG_LEVEL` | Nivel de logging | `DEBUG`, `INFO`, `WARNING` |

---

## 📝 Comandos Útiles

```bash
# Ver rutas disponibles
flask routes

# Shell interactivo de Flask
flask shell

# Ver configuración actual
flask config

# Crear usuario administrador (futuro)
# flask create-admin

# Seed de datos iniciales (futuro)
# flask seed
```

---

## 🐛 Troubleshooting

### Error de conexión a MySQL

1. Verificar que MySQL esté corriendo: `sudo systemctl status mysql`
2. Verificar credenciales en `.env`
3. Verificar que la base de datos exista
4. Verificar permisos del usuario MySQL

### Error de importación

1. Asegurar que el entorno virtual esté activado
2. Verificar que todas las dependencias estén instaladas: `pip list`
3. Reinstalar dependencias: `pip install -r requirements.txt --force-reinstall`

### Error de migraciones

1. Eliminar carpeta `migrations/`
2. Eliminar tabla `alembic_version` en la BD
3. Reinicializar: `flask db init`

---

## 📚 Documentación Adicional

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

---

## 👥 Equipo

Desarrollado para **Enlaces Costa Grande**

---

## 📄 Licencia

Privado - Todos los derechos reservados

---

## 🔄 Versiones

- **v1.0.0** - Fase 1: Setup y Base Técnica
  - Estructura del proyecto
  - Configuración Flask + SQLAlchemy
  - Endpoint de salud
  - Sistema de testing

---

**Última actualización**: Julio 2026
