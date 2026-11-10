# Plan de Implementación por Fases
## Portal de Verificación de Cobertura y Solicitud de Instalación

---

## Propósito del Plan

Este documento descompone el proyecto en fases de implementación secuenciales, cada una con alcance limitado y entregables concretos, para permitir:
- Ejecución incremental sin saturación
- Revisión humana entre fases
- Detección temprana de problemas
- Entrega de valor progresiva
- Mantenimiento de consistencia técnica y funcional

---

## Principios de Descomposición

1. **Base primero**: La infraestructura y modelo de datos deben estar sólidos antes de construir funcionalidad sobre ellos.
2. **Cobertura antes que prospecto**: El superadministrador debe poder administrar zonas antes de que los prospectos las consulten.
3. **Valor temprano**: Cada fase debe entregar funcionalidad usable, no solo código.
4. **Dependencias explícitas**: Cada fase declara qué necesita de fases anteriores.
5. **Revisión obligatoria**: Entre fases hay puntos de revisión para validar que todo funciona antes de avanzar.
6. **Alcance acotado**: Si una fase crece demasiado, se divide.
7. **Sin código**: Este plan define qué hacer, no cómo implementarlo.

---

## Lista de Fases

| # | Fase | Objetivo Principal |
|---|------|-------------------|
| 1 | Setup y Base Técnica | Establecer estructura del proyecto, dependencias y configuración base |
| 2 | Modelo de Datos y Migraciones | Crear esquema de base de datos completo con todas las entidades |
| 3 | Gestión de Cobertura (Superadmin) | Permitir administración de zonas, cobertura y planes |
| 4 | Portal Público - Búsqueda de Cobertura | Permitir a prospectos verificar cobertura por ubicación |
| 5 | Portal Público - Planes y Cotización | Mostrar planes disponibles y cotización estimada |
| 6 | Portal Público - Formulario de Solicitud | Permitir solicitud de instalación con validaciones |
| 7 | Panel Administrativo - Gestión de Solicitudes | Permitir visualización y gestión de solicitudes por ventas |
| 8 | Panel Administrativo - Notas y Seguimiento | Permitir agregar notas y cambiar estados de solicitudes |
| 9 | Análisis de Demanda por Zona | Proporcionar conteos y agrupaciones de solicitudes por zona |
| 10 | Endurecimiento y Validación | Seguridad, performance, validaciones y pruebas |

---

## Detalle de Fases.

### Fase 1: Setup y Base Técnica

#### Especificación Técnica (Spec-Driven Development)

**Objetivo**
Establecer la infraestructura técnica completa del proyecto con Python 3.12 + Flask, MySQL, SQLAlchemy y herramientas de desarrollo, creando una base sólida y funcional sobre la cual construir las fases siguientes.

**Alcance**

1. **Estructura del Proyecto**
   - Crear estructura de carpetas según PROJECT.md
   - Configurar entorno virtual de Python 3.12
   - Establecer archivos de configuración base (requirements.txt, .env.example)

2. **Backend (Flask)**
   - Instalar Flask y dependencias base desde requirements.txt
   - Configurar aplicación Flask con factory pattern
   - Establecer estructura de blueprints
   - Configurar CORS para frontend
   - Implementar middleware básico (logging, error handling)

3. **Base de Datos (MySQL + SQLAlchemy)**
   - Configurar conexión a MySQL con SQLAlchemy
   - Instalar Flask-SQLAlchemy y Flask-Migrate
   - Configurar Alembic para migraciones
   - Establecer configuración de pools de conexión
   - Crear script de inicialización de BD

4. **Configuración y Entorno**
   - Configurar python-dotenv para variables de entorno
   - Crear archivo .env.example con todas las variables necesarias
   - Establecer configuración por entorno (development, testing, production)
   - Configurar logging estructurado

5. **Testing**
   - Instalar pytest y pytest-cov
   - Configurar estructura de tests
   - Crear fixtures base
   - Establecer configuración de coverage

6. **Documentación**
   - Crear README.md con instrucciones de setup
   - Documentar variables de entorno
   - Documentar comandos disponibles

**Comandos Ejecutables**

```bash
# Crear entorno virtual de Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalación de dependencias
pip install -r requirements.txt

# Configuración inicial
cp .env.example .env
# Editar .env con credenciales locales de MySQL

# Inicializar migraciones con Alembic/Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Ejecutar servidor de desarrollo Flask
export FLASK_APP=app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

# Ejecutar tests con pytest
pytest
pytest --cov=app --cov-report=html

# Linting (opcional)
flake8 app/
black app/
```

**Estructura de Proyecto (Definición Explícita)**

```
estadia/
├── app/                              # Aplicación Flask principal
│   ├── __init__.py                   # Factory pattern (create_app)
│   ├── config.py                     # Configuración por entorno
│   ├── extensions.py                 # Extensiones Flask (db, migrate, cors)
│   ├── models/                       # Modelos SQLAlchemy (vacío en Fase 1)
│   │   └── __init__.py
│   ├── routes/                       # Blueprints Flask (vacío en Fase 1)
│   │   ├── __init__.py
│   │   └── health.py                 # Endpoint de salud
│   ├── services/                     # Lógica de negocio (vacío en Fase 1)
│   │   └── __init__.py
│   └── utils/                        # Utilidades auxiliares
│       └── __init__.py
├── migrations/                       # Migraciones Alembic (generado por flask db init)
│   ├── versions/                     # Archivos de migración
│   ├── env.py                        # Configuración Alembic
│   └── alembic.ini                   # Configuración Alembic
├── tests/                            # Tests pytest
│   ├── __init__.py
│   ├── conftest.py                   # Fixtures globales (app, client, db)
│   └── test_health.py                # Test de salud inicial
├── public/                           # Frontend estático (HTML/CSS/JS vanilla)
│   ├── css/                          # Estilos CSS
│   ├── js/                           # JavaScript vanilla
│   └── images/                       # Imágenes y activos
├── venv/                             # Entorno virtual Python (no commitear)
├── .env                              # Variables de entorno locales (no commitear)
├── .env.example                      # Template de variables de entorno
├── .gitignore                        # Ignorar venv/, .env, __pycache__/
├── requirements.txt                  # Dependencias Python (Flask, SQLAlchemy, etc.)
├── pytest.ini                        # Configuración pytest
├── README.md                         # Documentación del proyecto
└── IMPLEMENTATION_PHASES.md          # Plan de implementación
```

**Configuración de Flask-SQLAlchemy (app/extensions.py)**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
```

**Configuración de Alembic (app/config.py)**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
```

**Factory Pattern (app/__init__.py)**

```python
from flask import Flask
from .config import config_by_name
from .extensions import db, migrate, cors

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='../public')
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprints
    from .routes.health import health_bp
    app.register_blueprint(health_bp)
    
    return app
```

**Dependencias Python (requirements.txt)**

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
PyMySQL==1.1.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.3.0
cryptography==41.0.7
```

**Variables de Entorno (.env.example)**

```bash
# Flask
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Base de Datos
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/isp_portal
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=isp_portal

# Testing
TESTING_DATABASE_URL=mysql+pymysql://user:password@localhost:3306/enlaces_test

# Logging
LOG_LEVEL=DEBUG
```

**Estilo de Código**

```python
# app/__init__.py - Factory Pattern
from flask import Flask
from .config import config_by_name
from .extensions import db, migrate

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='../public')
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints (Fase 2+)
    # from .routes import main_bp
    # app.register_blueprint(main_bp)
    
    return app
```

**Estrategia de Testing**

- **Framework**: pytest con pytest-cov
- **Cobertura mínima**: 80% para código de negocio
- **Estructura**: tests/ espejo de app/
- **Fixtures**: conftest.py con fixtures para app, client, db
- **Tests de Fase 1**: 
  - Test de salud de la aplicación
  - Test de conexión a BD
  - Test de configuración de entorno

**Boundaries**

**Siempre:**
- Usar factory pattern para crear la app
- Mantener configuración separada por entorno
- Documentar todas las variables de entorno
- Ejecutar tests antes de completar la fase
- Seguir PEP 8 y convenciones de Flask

**Preguntar primero:**
- Cambios en la estructura de carpetas
- Agregar nuevas dependencias
- Modificar configuración de BD
- Cambiar puerto de desarrollo

**Nunca:**
- Hardcodear credenciales en el código
- Commitar archivo .env
- Ignorar errores de conexión a BD
- Saltar la configuración de testing

**Criterios de Aceptación**

1. ✅ El servidor Flask inicia sin errores en puerto 5000
2. ✅ La aplicación responde en endpoint `/health` con status 200
3. ✅ La conexión a MySQL se establece correctamente
4. ✅ SQLAlchemy está configurado y funcional
5. ✅ Alembic/Flask-Migrate está inicializado
6. ✅ Las variables de entorno se cargan desde .env
7. ✅ pytest ejecuta sin errores y genera reporte de coverage
8. ✅ La estructura de carpetas sigue el PROJECT.md
9. ✅ README.md contiene instrucciones completas de setup
10. ✅ El entorno virtual funciona correctamente

**Riesgos Identificados**

1. **Riesgo**: Problemas de conexión a MySQL
   - **Mitigación**: Verificar credenciales y permisos antes de iniciar
   - **Fallback**: Usar SQLite temporalmente para desarrollo

2. **Riesgo**: Conflictos de versiones de dependencias
   - **Mitigación**: Usar versiones específicas en requirements.txt
   - **Fallback**: Crear entorno virtual limpio

3. **Riesgo**: Configuración incorrecta de Alembic
   - **Mitigación**: Seguir documentación oficial de Flask-Migrate
   - **Fallback**: Configurar migraciones manualmente

**Tareas Iniciales**

- [ ] **Tarea 1.1**: Crear estructura de carpetas
  - **Acceptance**: Todas las carpetas existen según estructura definida
  - **Verify**: `tree -L 2` muestra estructura correcta
  - **Files**: Todas las carpetas del proyecto

- [ ] **Tarea 1.2**: Configurar entorno virtual e instalar dependencias
  - **Acceptance**: requirements.txt creado, entorno virtual funcional
  - **Verify**: `pip list` muestra Flask, SQLAlchemy, pytest instalados
  - **Files**: requirements.txt, venv/

- [ ] **Tarea 1.3**: Crear aplicación Flask con factory pattern
  - **Acceptance**: app/__init__.py con create_app() funcional
  - **Verify**: `flask run` inicia servidor sin errores
  - **Files**: app/__init__.py, app/config.py, app/extensions.py

- [ ] **Tarea 1.4**: Configurar variables de entorno
  - **Acceptance**: .env.example creado, python-dotenv funcional
  - **Verify**: Variables se cargan correctamente en la app
  - **Files**: .env.example, .gitignore

- [ ] **Tarea 1.5**: Configurar conexión a MySQL con SQLAlchemy
  - **Acceptance**: Conexión a BD establecida, extensiones inicializadas
  - **Verify**: Test de conexión pasa exitosamente
  - **Files**: app/extensions.py, app/config.py

- [ ] **Tarea 1.6**: Inicializar Alembic/Flask-Migrate
  - **Acceptance**: Carpeta migrations/ creada, configuración funcional
  - **Verify**: `flask db --help` muestra comandos disponibles
  - **Files**: migrations/, app/__init__.py

- [ ] **Tarea 1.7**: Configurar pytest y crear tests base
  - **Acceptance**: pytest ejecuta, coverage se genera
  - **Verify**: `pytest --cov=app` ejecuta sin errores
  - **Files**: pytest.ini, tests/conftest.py, tests/test_health.py

- [ ] **Tarea 1.8**: Crear endpoint de salud
  - **Acceptance**: GET /health retorna 200 OK
  - **Verify**: `curl http://localhost:5000/health` retorna status 200
  - **Files**: app/routes/health.py

- [ ] **Tarea 1.9**: Crear README.md con instrucciones
  - **Acceptance**: README contiene setup completo, comandos, variables
  - **Verify**: README es claro y completo
  - **Files**: README.md

- [ ] **Tarea 1.10**: Validación final de la Fase 1
  - **Acceptance**: Todos los criterios de aceptación cumplidos
  - **Verify**: Checklist completo, tests pasan, servidor funcional
  - **Files**: Todos

**Dependencias**
- Ninguna (primera fase)

**Entregables**
- Estructura de carpetas completa y funcional
- Aplicación Flask operativa con factory pattern
- Conexión a MySQL establecida y configurada
- SQLAlchemy y Alembic inicializados
- Sistema de variables de entorno funcional
- Suite de tests configurada y ejecutable
- README.md con instrucciones completas
- requirements.txt con todas las dependencias

**Fuera de Alcance**
- Modelos de datos específicos (Fase 2)
- Migraciones de tablas de negocio (Fase 2)
- Endpoints de negocio (Fases 3+)
- Interfaces de usuario (Fases 4+)
- Autenticación (Fase 3)
- Lógica de negocio (Fases 3+)

**Observaciones**
- Stack confirmado: Python 3.12 + Flask + MySQL + SQLAlchemy + Alembic + pytest
- El portal es público y accesible desde internet (RN-024)
- Esta fase establece la base técnica para todas las fases siguientes
- No implementar funcionalidad de negocio en esta fase
- Validar que todos los componentes funcionan antes de avanzar a Fase 2

---

### Fase 2: Modelo de Datos y Migraciones

**Objetivo**
Crear el esquema completo de base de datos con todas las entidades definidas en el PROJECT.md, incluyendo relaciones, campos de auditoría y constraints.

**Alcance**
- Crear migraciones para todas las entidades:
  - Municipio
  - Colonia/Comunidad
  - Cobertura
  - Plan
  - Disponibilidad de Plan por Zona
  - Solicitud de Instalación
  - Nota de Solicitud
  - Usuario Administrativo
- Implementar todas las relaciones definidas
- Agregar campos de auditoría (creado_por, fecha_creación, actualizado_por, fecha_modificación)
- Crear seeds iniciales para datos de prueba (municipios, colonias, planes de ejemplo)
- Implementar índices para consultas frecuentes

**Dependencias**
- Fase 1 completada (base de datos configurada)

**Entregables**
- Migraciones ejecutables y reversibles
- Esquema de base de datos completo
- Seeds con datos de prueba
- Documentación del modelo de datos
- Script de setup que crea base de datos desde cero

**Criterios de Revisión**
- ¿Todas las entidades del PROJECT.md están implementadas?
- ¿Las relaciones son correctas?
- ¿Los campos de auditoría están en todas las entidades?
- ¿Los seeds crean datos válidos?
- ¿Se puede ejecutar el setup completo sin errores?
- ¿El modelo soporta los casos de uso del PROJECT.md?

**Fuera de Alcance**
- Lógica de negocio
- APIs o endpoints
- Interfaces de usuario
- Validaciones complejas

**Observaciones**
- Esta fase es crítica: errores aquí afectan todas las fases siguientes
- Revisar cuidadosamente que el modelo refleje el PROJECT.md
- Los datos de prueba deben ser realistas para pruebas posteriores

---

### Fase 3: Gestión de Cobertura (Superadmin)

**Objetivo**
Implementar la interfaz y lógica para que el superadministrador pueda administrar el catálogo de zonas, cobertura y planes.

**Alcance**
- Autenticación de superadministrador (login/logout)
- CRUD de Municipios
- CRUD de Colonias/Comunidades (asociadas a municipios)
- CRUD de Cobertura (activar/desactivar por colonia)
- CRUD de Planes
- Asociación de planes a coberturas (Disponibilidad de Plan por Zona)
- Configuración de costos de instalación por zona/plan
- Vista jerárquica: Municipio → Colonia → Cobertura → Planes
- Validación al desactivar zona con solicitudes pendientes (RF-038)
- Campos de auditoría visibles (quién creó/modificó)

**Dependencias**
- Fase 2 completada (modelo de datos listo)

**Entregables**
- Sistema de autenticación funcional
- Interfaz para administrar municipios
- Interfaz para administrar colonias/comunidades
- Interfaz para activar/desactivar cobertura
- Interfaz para administrar planes
- Interfaz para asociar planes a zonas
- Interfaz para configurar costos de instalación
- Vista jerárquica del territorio
- Validaciones implementadas

**Criterios de Revisión**
- ¿El superadministrador puede hacer login?
- ¿Puede crear/editar/desactivar municipios y colonias?
- ¿Puede activar/desactivar cobertura?
- ¿Puede asociar planes a zonas con cobertura?
- ¿Puede configurar costos de instalación?
- ¿La vista jerárquica muestra correctamente la estructura?
- ¿Las validaciones funcionan (ej: no desactivar zona con solicitudes)?
- ¿Los campos de auditoría se registran correctamente?

**Fuera de Alcance**
- Portal público
- Panel de ventas
- Análisis de demanda
- Solicitudes de instalación

**Observaciones**
- Esta fase habilita la operación del superadministrador
- Es la base para que existan zonas con cobertura que los prospectos puedan consultar
- El superadministrador define el costo estándar base y puede ajustarlo por zona (RN-003, CA-020)

---

### Fase 4: Portal Público - Búsqueda de Cobertura

**Objetivo**
Implementar la funcionalidad básica del portal público para que prospectos puedan verificar si su ubicación tiene cobertura.

**Alcance**
- Landing page con buscador de ubicación
- Selector cascada: Municipio → Colonia/Comunidad
- Búsqueda con autocompletado y búsqueda parcial (RF-001, RF-002)
- Lógica para verificar cobertura (RC-001)
- Mensaje claro si hay cobertura
- Mensaje claro si no hay cobertura
- Diseño responsivo mobile-first
- Experiencia visual comercial tipo telecom

**Dependencias**
- Fase 3 completada (deben existir zonas con cobertura)

**Entregables**
- Landing page funcional
- Selector de municipio con búsqueda
- Selector de colonia/comunidad con búsqueda
- Lógica de verificación de cobertura
- Mensajes de resultado (con/sin cobertura)
- Diseño responsivo
- Estilo visual alineado con branding

**Criterios de Revisión**
- ¿El prospecto puede seleccionar municipio y colonia?
- ¿La búsqueda funciona con autocompletado?
- ¿El sistema indica correctamente si hay cobertura?
- ¿Los mensajes son claros?
- ¿Funciona en móvil y desktop?
- ¿El diseño es profesional y comercial?
- ¿El tiempo de respuesta es menor a 2 segundos (RNF-001)?

**Fuera de Alcance**
- Mostrar planes
- Cotización
- Formulario de solicitud
- Flujo para dejar datos sin cobertura

**Observaciones**
- Esta fase entrega el primer valor al prospecto
- La experiencia visual es crítica para conversión
- El branding debe seguir los lineamientos de Internet Regional

---

### Fase 5: Portal Público - Planes y Cotización

**Objetivo**
Mostrar los planes disponibles en la zona con cobertura y calcular cotización estimada.

**Alcance**
- Mostrar planes disponibles en zona con cobertura (RF-004)
- Formato de tarjetas (pricing table)
- Cada tarjeta muestra: nombre, velocidades, precio mensual (RF-005)
- Selección de plan
- Cálculo de cotización estimada: costo estándar base + ajuste por zona + mensualidad (RF-006, RN-003)
- Mostrar cotización al prospecto con aviso claro de que es estimada (CA-008)
- Plan destacado visualmente (campo "destacado" del modelo)
- Ordenamiento de planes (campo "orden" del modelo)

**Dependencias**
- Fase 4 completada (búsqueda de cobertura funcionando)
- Fase 3 completada (planes asociados a zonas)

**Entregables**
- Visualización de planes en formato tarjetas
- Información completa de cada plan
- Selección de plan funcional
- Cálculo de cotización
- Visualización de cotización
- Plan destacado visualmente
- Ordenamiento correcto de planes

**Criterios de Revisión**
- ¿Se muestran solo planes disponibles en la zona?
- ¿La información de cada plan es completa?
- ¿Se puede seleccionar un plan?
- ¿La cotización se calcula correctamente?
- ¿El plan destacado se ve diferente?
- ¿Los planes están en el orden correcto?
- ¿La experiencia es clara y comercial?

**Fuera de Alcance**
- Formulario de solicitud
- Flujo para dejar datos sin cobertura
- Validación de duplicados

**Observaciones**
- Esta fase complementa la búsqueda con información de planes
- La presentación visual de planes es crítica para conversión
- La cotización debe ser clara sobre qué incluye

---

### Fase 6: Portal Público - Formulario de Solicitud

**Objetivo**
Implementar el formulario completo para que prospectos soliciten instalación, incluyendo validaciones y manejo de leads sin cobertura.

**Alcance**
- Formulario de solicitud con campos obligatorios (RF-007):
  - Nombre completo
  - Teléfono (10 dígitos)
  - Dirección específica
  - Plan seleccionado (prellenado)
  - Ubicación (prellenada)
- Validaciones de formulario (RF-008, RF-009, RN-008)
- Validación de duplicados: mismo teléfono en últimos 7 días (RF-013, RN-011)
- Mensaje de confirmación con número de solicitud (RF-010)
- Registro de solicitud con estado "pendiente" y origen "portal" (RF-011, RN-004)
- Aviso visible de que la contratación formal requiere contrato firmado (RF-014, CA-009)
- Flujo alternativo: dejar datos cuando no hay cobertura (RF-012, RN-009)
- Registro como "lead_sin_cobertura" (RN-022)
- Manejo de errores y mensajes claros

**Dependencias**
- Fase 5 completada (plan seleccionado)
- Fase 4 completada (ubicación seleccionada)

**Entregables**
- Formulario completo funcional
- Validaciones de campos
- Validación de duplicados
- Mensaje de confirmación
- Registro de solicitud en base de datos
- Flujo para leads sin cobertura
- Manejo de errores

**Criterios de Revisión**
- ¿Todos los campos obligatorios están presentes?
- ¿Las validaciones funcionan correctamente?
- ¿Se detectan solicitudes duplicadas?
- ¿El mensaje de confirmación se muestra?
- ¿La solicitud se registra correctamente en BD?
- ¿El flujo sin cobertura funciona?
- ¿Los leads sin cobertura se registran como tipo "lead_sin_cobertura"?
- ¿Los mensajes de error son claros (RNF-007)?

**Fuera de Alcance**
- Panel administrativo
- Gestión de solicitudes por ventas
- Análisis de demanda

**Observaciones**
- Esta fase completa el flujo del prospecto
- Las validaciones son críticas para calidad de datos
- El aviso de contrato firmado debe ser visible antes del envío

---

### Fase 7: Panel Administrativo - Gestión de Solicitudes

**Objetivo**
Implementar el panel para que el equipo de ventas pueda visualizar y gestionar las solicitudes recibidas.

**Alcance**
- Autenticación de administrador/ventas (RF-014)
- Tabla de solicitudes con columnas: fecha, nombre, teléfono, ubicación, plan, origen, estado (RF-015, RF-016)
- Filtros por estado: pendiente, contactado, agendado, cancelado, duplicado (RF-017)
- Ordenamiento por fecha (más recientes primero) (RF-018)
- Vista de detalles en modal o panel lateral (RF-019, RF-020)
- Cambio de estado de solicitud (RF-021)
- Marcar solicitud como duplicada (RF-026, RN-012)
- Exportación a CSV/Excel respetando filtros (RF-025)

**Dependencias**
- Fase 6 completada (existen solicitudes en el sistema)

**Entregables**
- Sistema de autenticación para administradores
- Tabla de solicitudes funcional
- Filtros por estado
- Ordenamiento por fecha
- Vista de detalles
- Cambio de estado
- Marcar como duplicado
- Exportación a CSV/Excel

**Criterios de Revisión**
- ¿El administrador puede hacer login?
- ¿La tabla muestra todas las solicitudes?
- ¿Los filtros funcionan correctamente?
- ¿El ordenamiento es correcto?
- ¿La vista de detalles muestra toda la información?
- ¿Se puede cambiar el estado?
- ¿Se puede marcar como duplicada?
- ¿La exportación incluye los datos correctos?
- ¿Las solicitudes duplicadas no cuentan para métricas (RN-012)?

**Fuera de Alcance**
- Notas internas
- Análisis de demanda
- Gestión de cobertura

**Observaciones**
- Esta fase habilita la operación del equipo de ventas
- La tabla debe ser eficiente para manejar muchas solicitudes
- Todas las solicitudes son visibles para todo el equipo de ventas (P-001 pendiente de definir si habrá asignación automática)

---

### Fase 8: Panel Administrativo - Notas y Seguimiento

**Objetivo**
Implementar el sistema de notas internas para que el equipo de ventas pueda dar seguimiento a las solicitudes.

**Alcance**
- Agregar notas internas a solicitud (RF-022)
- Registro de timestamp y usuario que agregó la nota
- Visualización de historial completo de notas en orden cronológico (RF-023)
- Notas no visibles para prospecto (RN-010)
- Validación al desactivar zona con solicitudes pendientes activas (RF-038, RN-021)

**Dependencias**
- Fase 7 completada (gestión de solicitudes funcionando)

**Entregables**
- Funcionalidad para agregar notas
- Historial de notas visible
- Timestamp y usuario en cada nota
- Notas separadas de vista pública
- Validación de desactivación de zona

**Criterios de Revisión**
- ¿Se pueden agregar notas?
- ¿El historial se muestra en orden cronológico?
- ¿Cada nota tiene timestamp y usuario?
- ¿Las notas no son visibles para prospectos?
- ¿La validación de desactivación funciona?

**Fuera de Alcance**
- Análisis de demanda
- Refinamientos visuales
- Notificaciones automáticas

**Observaciones**
- Esta fase completa el seguimiento de solicitudes
- Las notas son críticas para coordinación de equipo
- El historial debe ser claro y fácil de leer

---

### Fase 9: Análisis de Demanda por Zona

**Objetivo**
Implementar funcionalidades de análisis básico para identificar concentración de solicitudes y oportunidades de expansión.

**Alcance**
- Vista de mapeo básico: solicitudes agrupadas por municipio/colonia con conteos (RF-024)
- Análisis de demanda: conteo por municipio y colonia (RF-027)
- Diferenciación entre solicitudes con cobertura y sin cobertura (RF-027, RN-018)
- Filtros por rango de fechas y estado (RF-028)
- Indicadores visuales de zonas con alta demanda: top 10 colonias (RF-029)
- Agrupación por estado (pendiente, contactado, agendado, cancelado)

**Dependencias**
- Fase 7 completada (existen solicitudes)
- Fase 3 completada (existen zonas con/sin cobertura)

**Entregables**
- Vista de mapeo básico (tabla agrupada)
- Conteos de solicitudes por zona
- Diferenciación con/sin cobertura
- Filtros por fecha y estado
- Top 10 zonas con más solicitudes
- Agrupación por estado

**Criterios de Revisión**
- ¿Los conteos son correctos?
- ¿Se diferencian solicitudes con/sin cobertura?
- ¿Los filtros funcionan?
- ¿El top 10 se calcula correctamente?
- ¿La información es útil para identificar demanda?
- ¿Ayuda a identificar zonas candidatas para expansión?

**Fuera de Alcance**
- Mapas interactivos
- Gráficos complejos
- Análisis predictivo
- Métricas avanzadas

**Observaciones**
- Esta fase proporciona visibilidad para decisiones de expansión
- El análisis debe ser simple pero útil
- Los datos de leads sin cobertura son especialmente valiosos

---

### Fase 10: Endurecimiento y Validación

**Objetivo**
Validar que todo el sistema funciona correctamente, mejorar performance, asegurar cumplimiento de requisitos no funcionales y preparar para producción.

**Alcance**
- Validación de todos los requisitos funcionales del PROJECT.md
- Pruebas de performance (RNF-001, RNF-002, RNF-003)
- Validación de responsividad en múltiples dispositivos (RNF-004, RNF-018, RNF-019)
- Pruebas de seguridad (RNF-010, RNF-011, RNF-012, RNF-013)
- Validación de accesibilidad (RNF-020, RNF-021, RNF-022)
- Pruebas de usabilidad (RNF-005, RNF-006, RNF-007, RNF-008)
- Validación de mantenibilidad (RNF-014, RNF-015, RNF-016, RNF-017)
- Pruebas de compatibilidad de navegadores (RNF-018)
- Validación de todos los criterios de aceptación (CA-001 a CA-025)
- Corrección de bugs y problemas encontrados
- Optimización de consultas y performance
- Documentación final

**Dependencias**
- Todas las fases anteriores completadas

**Entregables**
- Sistema completamente funcional
- Pruebas de performance documentadas
- Pruebas de seguridad documentadas
- Pruebas de accesibilidad documentadas
- Bugs corregidos
- Performance optimizado
- Documentación final
- Sistema listo para producción

**Criterios de Revisión**
- ¿Todos los RF están implementados y funcionando?
- ¿Todos los CA se cumplen?
- ¿Los RNF se cumplen (performance, seguridad, accesibilidad)?
- ¿No hay bugs críticos?
- ¿El sistema es estable?
- ¿La documentación está completa?
- ¿Está listo para producción?

**Fuera de Alcance**
- Nuevas funcionalidades
- Cambios de diseño mayores
- Integraciones no planificadas

**Observaciones**
- Esta fase es crítica antes de lanzar a producción
- Puede revelar problemas de fases anteriores que requieren corrección
- Decisiones pendientes que deben resolverse:
  - P-004: Requisitos legales de protección de datos
  - P-005: Backup y retención de datos

---

## Orden de Ejecución Recomendado

```
Fase 1: Setup y Base Técnica
    ↓
Fase 2: Modelo de Datos y Migraciones
    ↓
Fase 3: Gestión de Cobertura (Superadmin)
    ↓
Fase 4: Portal Público - Búsqueda de Cobertura
    ↓
Fase 5: Portal Público - Planes y Cotización
    ↓
Fase 6: Portal Público - Formulario de Solicitud
    ↓
Fase 7: Panel Administrativo - Gestión de Solicitudes
    ↓
Fase 8: Panel Administrativo - Notas y Seguimiento
    ↓
Fase 9: Análisis de Demanda por Zona
    ↓
Fase 10: Endurecimiento y Validación
```

---

## Qué Revisar Antes de Pasar a la Siguiente Fase

### Entre cada fase, revisar:

1. **Funcionalidad**: ¿Todo lo implementado funciona correctamente?
2. **Criterios de revisión**: ¿Se cumplen todos los criterios de la fase?
3. **Consistencia**: ¿La implementación es consistente con el PROJECT.md?
4. **Calidad de código**: ¿El código sigue los principios de SRP y arquitectura por capas?
5. **Datos**: ¿Los datos de prueba son realistas y suficientes?
6. **Experiencia de usuario**: ¿La experiencia es clara y profesional?
7. **Performance**: ¿El performance es aceptable?
8. **Documentación**: ¿Los entregables están documentados?

### Puntos de revisión críticos:

- **Después de Fase 2**: Validar que el modelo de datos refleja completamente el PROJECT.md
- **Después de Fase 3**: Validar que el superadministrador puede operar el sistema
- **Después de Fase 6**: Validar que el flujo completo del prospecto funciona
- **Después de Fase 8**: Validar que el equipo de ventas puede operar el sistema
- **Después de Fase 10**: Validación final antes de producción

---

## Decisiones Pendientes del PROJECT.md

Las siguientes preguntas del PROJECT.md deben resolverse antes o durante la implementación:

- **P-001**: ¿Asignación automática de solicitudes a vendedores? → Afecta Fase 7
- **P-002**: ¿Notificaciones de nuevas solicitudes? → Afecta Fase 7
- **P-003**: ¿Validación de teléfono real? → Afecta Fase 6
- **P-004**: ¿Requisitos legales de protección de datos? → Afecta Fase 10
- **P-005**: ¿Backup y retención de datos? → Afecta Fase 10

### Decisiones Ya Cerradas (No Requieren Acción)

Las siguientes decisiones ya están definidas en el PROJECT.md y no deben tratarse como pendientes:

- ✅ El portal es público y accesible desde internet (RN-024)
- ✅ El branding es de Internet Regional
- ✅ La cobertura se administra por catálogo estructurado (RN-001)
- ✅ Existe un costo estándar base de instalación definido por el superadministrador (CA-020)
- ✅ El superadministrador puede ajustar el costo por zona (RN-003)
- ✅ La cotización mostrada al prospecto es estimada (CA-008)
- ✅ La contratación formal requiere contrato firmado (CA-009, RN-025)
- ✅ La firma y gestión documental avanzada del contrato no forman parte de V1 (E-015 a E-019)
- ✅ El mapa no es central en V1 (E-001)
- ✅ El análisis de demanda básico por zona sí forma parte del alcance (RF-027 a RF-029)
- ✅ Las solicitudes sin cobertura se registran como leads sin cobertura (RN-022)

---

## Qué Queda Fuera de Este Plan

Este plan cubre exclusivamente la V1 definida en el PROJECT.md. Quedan fuera:

- Visualización territorial tipo mapa (Fase 3 futura)
- Cobertura parcial o condicional (preparada en modelo, no implementada)
- Análisis de demanda avanzado (tendencias, comparativas)
- Notificaciones automáticas (email, SMS)
- Integraciones con sistemas externos (CRM, facturación, provisión)
- Asignación automática de solicitudes a vendedores
- Historial personal de solicitudes para prospectos
- Agendamiento de instalación en línea
- Multi-idioma
- Aplicación móvil nativa

Estas capacidades están preparadas en el modelo de datos o son evoluciones futuras, pero no se implementan en V1.

---

## Historial de Actualizaciones

| Fecha | Descripción |
|-------|-------------|
| 2026-07-30 | Versión inicial del plan de implementación |
| 2026-07-30 | Alineación con PROJECT.md v7.0: eliminación de decisiones cerradas, corrección de referencias a costos (estándar base + ajuste por zona), contrato firmado, portal público, y compresión de preguntas pendientes a solo 5 realmente abiertas |
| 2026-07-30 | Fase 1: Especificación técnica completa con spec-driven-development. Stack confirmado: Python 3.12 + Flask + MySQL + SQLAlchemy + Alembic + pytest. Incluye objetivos, alcance, comandos, estructura, estilo de código, estrategia de testing, boundaries, criterios de aceptación, riesgos y 10 tareas descompuestas |

---

**Fin del documento**
