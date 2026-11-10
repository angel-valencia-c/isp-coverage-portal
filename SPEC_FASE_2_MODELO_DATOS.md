# Spec: Fase 2 - Modelo de Datos y Migraciones

## Objective

Crear el esquema completo de base de datos para el Portal de Verificación de Cobertura de Internet Regional, implementando todas las entidades, relaciones, campos de auditoría, índices y seeds de datos de prueba definidos en el PROJECT.md.

**¿Por qué?**
El modelo de datos es la base sobre la cual se construirán todas las funcionalidades del sistema (Fases 3-10). Un modelo incorrecto o incompleto requerirá refactor costoso en fases posteriores.

**¿Para quién?**
- Desarrolladores backend que implementarán la lógica de negocio
- Desarrolladores frontend que consumirán las APIs
- Equipo de QA que validará el comportamiento del sistema

**¿Qué significa éxito?**
- Todas las 8 entidades del PROJECT.md están implementadas como modelos SQLAlchemy
- Todas las relaciones están correctamente definidas y probadas
- Los campos de auditoría están presentes en todas las entidades
- Las migraciones son ejecutables y reversibles
- Los seeds crean datos válidos y realistas
- Los tests unitarios verifican la integridad del modelo
- El esquema soporta todos los casos de uso definidos en el PROJECT.md

---

## Tech Stack

- **Base de datos**: MySQL 8.0+ (producción/desarrollo), SQLite en memoria (testing)
- **ORM**: SQLAlchemy 2.0.51 + Flask-SQLAlchemy 3.1.1
- **Migraciones**: Alembic 1.18.5 + Flask-Migrate 4.0.5
- **Testing**: pytest 7.4.3 + pytest-flask 1.3.0
- **Python**: 3.14.6 (versión estable adoptada en Fase 1)

### Convenciones del Proyecto

**Nombres de tablas**: Plural snake_case (regla oficial del proyecto)
- Ejemplos: `municipios`, `colonias_comunidades`, `solicitudes_instalacion`
- Esta convención se aplicará consistentemente en todas las fases

**Nombres de columnas**: Snake_case
- Ejemplos: `fecha_creacion`, `municipio_id`, `nombre_prospecto`

**Claves primarias**: `id` (Integer, autoincrement)

**Claves foráneas**: `{entidad}_id` (ej: `municipio_id`, `colonia_id`)

---

## Commands

```bash
# Activar entorno virtual
source venv/bin/activate

# Crear nueva migración
flask db migrate -m "descripción del cambio"

# Aplicar migración
flask db upgrade

# Revertir última migración
flask db downgrade

# Ver historial de migraciones
flask db history

# Ver estado actual
flask db current

# Ejecutar seeds (script Python directo)
python seeds/initial_data.py

# Resetear base de datos (desarrollo)
flask db downgrade base
flask db upgrade
python seeds/initial_data.py

# Ejecutar tests de modelos
pytest tests/models/ -v

# Ejecutar tests con coverage
pytest tests/models/ --cov=app/models --cov-report=html
```

### Comando CLI para Seeds

Se implementará un comando Flask CLI personalizado en `app/cli.py`:

```python
# app/cli.py
import click
from flask import current_app
from app.extensions import db

def register_commands(app):
    @app.cli.command('seed')
    def seed_command():
        """Ejecutar seeds de datos iniciales"""
        from seeds.initial_data import run_seeds
        click.echo('Ejecutando seeds...')
        run_seeds()
        click.echo('Seeds completados exitosamente.')
```

Registro en `app/__init__.py`:
```python
from .cli import register_commands

def create_app(config_name='development'):
    # ... código existente ...
    register_commands(app)
    return app
```

Uso:
```bash
flask seed
```

---

## Project Structure

```
estadia/
├── app/
│   ├── models/                          # Modelos SQLAlchemy
│   │   ├── __init__.py                  # Exportar todos los modelos
│   │   ├── base.py                      # Clase base con campos de auditoría
│   │   ├── municipio.py                 # Modelo Municipio
│   │   ├── colonia.py                   # Modelo Colonia/Comunidad
│   │   ├── cobertura.py                 # Modelo Cobertura
│   │   ├── plan.py                      # Modelo Plan
│   │   ├── disponibilidad_plan.py       # Modelo DisponibilidadPlanZona
│   │   ├── solicitud.py                 # Modelo SolicitudInstalacion
│   │   ├── nota_solicitud.py            # Modelo NotaSolicitud
│   │   └── usuario.py                   # Modelo UsuarioAdministrativo
│   └── ...
├── migrations/
│   └── versions/                        # Archivos de migración generados
├── seeds/                               # Scripts de seeds
│   ├── __init__.py
│   └── initial_data.py                  # Seeds iniciales
├── tests/
│   ├── models/                          # Tests de modelos
│   │   ├── __init__.py
│   │   ├── test_municipio.py
│   │   ├── test_colonia.py
│   │   ├── test_cobertura.py
│   │   ├── test_plan.py
│   │   ├── test_disponibilidad_plan.py
│   │   ├── test_solicitud.py
│   │   ├── test_nota_solicitud.py
│   │   └── test_usuario.py
│   └── ...
└── ...
```

---

## Code Style

### Clase Base con Campos de Auditoría

```python
# app/models/base.py
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    """
    Clase base abstracta con campos de auditoría.
    
    Campos de auditoría:
    - creado_por: FK a UsuarioAdministrativo (nullable para registros del portal)
    - fecha_creacion: Timestamp de creación (auto-generado)
    - actualizado_por: FK a UsuarioAdministrativo (nullable para registros del portal)
    - fecha_modificacion: Timestamp de última modificación (auto-actualizado)
    
    Manejo de usuarios anónimos:
    - Las solicitudes creadas desde el portal público tendrán creado_por=NULL
    - Las solicitudes creadas/modificadas por administradores tendrán el ID del usuario
    - Esto permite distinguir entre registros del sistema y registros de usuarios
    """
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios_administrativos.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actualizado_por = db.Column(db.Integer, db.ForeignKey('usuarios_administrativos.id'), nullable=True)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones con usuario que creó/modificó (opcionales)
    creador = db.relationship('UsuarioAdministrativo', foreign_keys=[creado_por], backref='registros_creados')
    actualizador = db.relationship('UsuarioAdministrativo', foreign_keys=[actualizado_por], backref='registros_actualizados')
```

### Modelo Ejemplo: Cobertura

```python
# app/models/cobertura.py
from app.extensions import db
from .base import BaseModel

class Cobertura(BaseModel):
    """
    Cobertura de servicio en una colonia/comunidad.
    
    Campo reglas (JSON):
    - En MySQL: Usa tipo JSON nativo
    - En SQLite (testing): Usa tipo Text con serialización manual
    - El modelo usa db.JSON que SQLAlchemy adapta automáticamente según el dialecto
    - Para testing con SQLite, se serializa/deserializa como string JSON
    """
    __tablename__ = 'coberturas'
    
    colonia_id = db.Column(db.Integer, db.ForeignKey('colonias_comunidades.id'), nullable=False, unique=True, index=True)
    activa = db.Column(db.Boolean, default=True, nullable=False, index=True)
    tipo_cobertura = db.Column(db.String(20), nullable=False, default='total', index=True)
    fecha_activacion = db.Column(db.DateTime, nullable=True)
    fecha_desactivacion = db.Column(db.DateTime, nullable=True)
    notas = db.Column(db.Text, nullable=True)
    
    # Campo JSON para reglas futuras (compatible con MySQL y SQLite)
    # En MySQL se almacena como JSON nativo, en SQLite como Text
    reglas = db.Column(db.JSON, nullable=True)
    
    # Relaciones
    colonia = db.relationship('ColoniaComunidad', backref=db.backref('cobertura', uselist=False))
    planes_disponibles = db.relationship('DisponibilidadPlanZona', backref='cobertura', lazy='dynamic', cascade='all, delete-orphan')
    
    # Tipos válidos
    TIPOS_VALIDOS = ['total', 'parcial', 'condicional', 'planificada']
    
    def __repr__(self):
        return f'<Cobertura {self.colonia_id} - {self.tipo_cobertura}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'colonia_id': self.colonia_id,
            'activa': self.activa,
            'tipo_cobertura': self.tipo_cobertura,
            'fecha_activacion': self.fecha_activacion.isoformat() if self.fecha_activacion else None,
            'fecha_desactivacion': self.fecha_desactivacion.isoformat() if self.fecha_desactivacion else None,
            'notas': self.notas,
            'reglas': self.reglas,  # JSON se serializa automáticamente
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }
```

### Modelo Ejemplo: Municipio

```python
# app/models/municipio.py
from app.extensions import db
from .base import BaseModel

class Municipio(BaseModel):
    """
    Municipio del estado de Guerrero donde opera Internet Regional.
    
    Relaciones:
    - Un municipio tiene muchas colonias/comunidades
    """
    __tablename__ = 'municipios'
    
    nombre = db.Column(db.String(100), nullable=False, unique=True, index=True)
    estado = db.Column(db.String(50), nullable=False, default='Guerrero')
    activo = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    # Relaciones
    colonias = db.relationship('ColoniaComunidad', backref='municipio', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Municipio {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }
```

### Modelo Ejemplo: SolicitudInstalacion

```python
# app/models/solicitud.py
from app.extensions import db
from .base import BaseModel

class SolicitudInstalacion(BaseModel):
    """
    Solicitud de instalación de servicio de internet.
    
    Tipos:
    - solicitud_cobertura: Prospecto con cobertura disponible
    - lead_sin_cobertura: Prospecto sin cobertura (lead para expansión)
    """
    __tablename__ = 'solicitudes_instalacion'
    
    # Datos del prospecto
    nombre_prospecto = db.Column(db.String(200), nullable=False, index=True)
    telefono_contacto = db.Column(db.String(10), nullable=False, index=True)
    direccion_especifica = db.Column(db.Text, nullable=True)
    
    # Ubicación
    municipio_id = db.Column(db.Integer, db.ForeignKey('municipios.id'), nullable=False, index=True)
    colonia_id = db.Column(db.Integer, db.ForeignKey('colonias_comunidades.id'), nullable=False, index=True)
    
    # Plan y cotización
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id'), nullable=True, index=True)
    costo_instalacion_cotizado = db.Column(db.Numeric(10, 2), nullable=True)
    precio_mensual_cotizado = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Estado y seguimiento
    estado = db.Column(db.String(20), nullable=False, default='pendiente', index=True)
    origen = db.Column(db.String(20), nullable=False, default='portal', index=True)
    tipo = db.Column(db.String(30), nullable=False, default='solicitud_cobertura', index=True)
    
    # Duplicados
    solicitud_duplicada_de = db.Column(db.Integer, db.ForeignKey('solicitudes_instalacion.id'), nullable=True)
    
    # Relaciones
    municipio = db.relationship('Municipio', backref='solicitudes')
    colonia = db.relationship('ColoniaComunidad', backref='solicitudes')
    plan = db.relationship('Plan', backref='solicitudes')
    notas = db.relationship('NotaSolicitud', backref='solicitud', lazy='dynamic', cascade='all, delete-orphan')
    duplicada_de = db.relationship('SolicitudInstalacion', remote_side=[id], backref='duplicadas')
    
    # Índices compuestos para consultas frecuentes
    __table_args__ = (
        db.Index('idx_solicitud_estado_fecha', 'estado', 'fecha_creacion'),
        db.Index('idx_solicitud_municipio_colonia', 'municipio_id', 'colonia_id'),
    )
    
    # Validaciones de estado
    ESTADOS_VALIDOS = ['pendiente', 'contactado', 'agendado', 'cancelado', 'duplicado']
    ORIGENES_VALIDOS = ['portal', 'telefono', 'whatsapp', 'presencial', 'otro']
    TIPOS_VALIDOS = ['solicitud_cobertura', 'lead_sin_cobertura']
    
    def __repr__(self):
        return f'<SolicitudInstalacion {self.id} - {self.nombre_prospecto}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_prospecto': self.nombre_prospecto,
            'telefono_contacto': self.telefono_contacto,
            'direccion_especifica': self.direccion_especifica,
            'municipio_id': self.municipio_id,
            'colonia_id': self.colonia_id,
            'plan_id': self.plan_id,
            'costo_instalacion_cotizado': float(self.costo_instalacion_cotizado) if self.costo_instalacion_cotizado else None,
            'precio_mensual_cotizado': float(self.precio_mensual_cotizado) if self.precio_mensual_cotizado else None,
            'estado': self.estado,
            'origen': self.origen,
            'tipo': self.tipo,
            'solicitud_duplicada_de': self.solicitud_duplicada_de,
            'fecha_solicitud': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }
```

---

## Testing Strategy

### Framework y Ubicación
- **Framework**: pytest con pytest-flask
- **Ubicación**: `tests/models/`
- **Cobertura esperada**: 90%+ para modelos

### Manejo de JSON en Testing (SQLite)

El campo `reglas` en Cobertura usa tipo `db.JSON` que SQLAlchemy adapta automáticamente:

**En MySQL (desarrollo/producción)**:
- Se almacena como JSON nativo
- Consultas JSON funcionan normalmente

**En SQLite (testing)**:
- Se almacena como TEXT con serialización JSON
- SQLAlchemy maneja la serialización/deserialización automáticamente
- Los tests pueden asignar diccionarios Python directamente: `cobertura.reglas = {"key": "value"}`
- Al leer, se obtiene el diccionario Python automáticamente

**Ejemplo de test**:
```python
def test_cobertura_con_reglas(self, app, db_session):
    """Test: El campo reglas acepta JSON en ambos dialectos"""
    cobertura = Cobertura(
        colonia_id=1,
        reglas={"capacidad_maxima": 100, "requiere_validacion": True}
    )
    db_session.add(cobertura)
    db_session.commit()
    
    # Recargar desde BD
    cobertura_db = db_session.query(Cobertura).first()
    assert cobertura_db.reglas["capacidad_maxima"] == 100
    assert cobertura_db.reglas["requiere_validacion"] is True
```

### Niveles de Testing

#### 1. Tests Unitarios de Modelos
```python
# tests/models/test_municipio.py
import pytest
from app.models.municipio import Municipio
from app.extensions import db

class TestMunicipioModel:
    """Tests para el modelo Municipio"""
    
    def test_crear_municipio(self, app, db_session):
        """Test: Se puede crear un municipio válido"""
        municipio = Municipio(nombre='Acapulco', estado='Guerrero')
        db_session.add(municipio)
        db_session.commit()
        
        assert municipio.id is not None
        assert municipio.nombre == 'Acapulco'
        assert municipio.activo is True
    
    def test_municipio_nombre_unico(self, app, db_session):
        """Test: El nombre del municipio debe ser único"""
        municipio1 = Municipio(nombre='Acapulco')
        municipio2 = Municipio(nombre='Acapulco')
        
        db_session.add(municipio1)
        db_session.commit()
        
        db_session.add(municipio2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_municipio_tiene_colonias(self, app, db_session):
        """Test: Un municipio puede tener muchas colonias"""
        from app.models.colonia import ColoniaComunidad
        
        municipio = Municipio(nombre='Acapulco')
        db_session.add(municipio)
        db_session.commit()
        
        colonia1 = ColoniaComunidad(nombre='Colonia 1', municipio_id=municipio.id)
        colonia2 = ColoniaComunidad(nombre='Colonia 2', municipio_id=municipio.id)
        db_session.add_all([colonia1, colonia2])
        db_session.commit()
        
        assert municipio.colonias.count() == 2
```

#### 2. Tests de Relaciones
```python
# tests/models/test_relaciones.py
class TestRelaciones:
    """Tests para verificar relaciones entre modelos"""
    
    def test_relacion_municipio_colonia(self, app, db_session):
        """Test: Relación uno a muchos entre Municipio y Colonia"""
        # Implementar test
    
    def test_relacion_colonia_cobertura(self, app, db_session):
        """Test: Relación uno a uno entre Colonia y Cobertura"""
        # Implementar test
    
    def test_relacion_cobertura_planes(self, app, db_session):
        """Test: Relación muchos a muchos entre Cobertura y Plan"""
        # Implementar test
```

#### 3. Tests de Constraints
```python
# tests/models/test_constraints.py
class TestConstraints:
    """Tests para verificar constraints de base de datos"""
    
    def test_telefono_longitud(self, app, db_session):
        """Test: Teléfono debe tener exactamente 10 dígitos"""
        # Implementar test
    
    def test_estado_valido(self, app, db_session):
        """Test: Estado debe ser uno de los valores permitidos"""
        # Implementar test
```

### Comandos de Verificación

```bash
# Ejecutar todos los tests de modelos
pytest tests/models/ -v

# Ejecutar con coverage
pytest tests/models/ --cov=app/models --cov-report=html

# Ejecutar un test específico
pytest tests/models/test_municipio.py::TestMunicipioModel::test_crear_municipio -v
```

---

## Boundaries

### Always (Siempre)

- ✅ Crear clase base `BaseModel` con campos de auditoría reutilizables
- ✅ Implementar todos los campos definidos en PROJECT.md sin omitir ninguno
- ✅ Definir relaciones bidireccionales con `backref` o `back_populates`
- ✅ Agregar índices para claves foráneas y campos de búsqueda frecuente
- ✅ Escribir docstrings explicando el propósito de cada modelo y relación
- ✅ Implementar método `to_dict()` en cada modelo para serialización
- ✅ Crear tests unitarios para cada modelo verificando creación y relaciones
- ✅ Usar tipos de datos apropiados (String, Integer, DateTime, Numeric, Boolean, Text, JSON)
- ✅ Definir constraints a nivel de base de datos (unique, not null, foreign key)
- ✅ Validar que las migraciones sean ejecutables y reversibles

### Ask First (Preguntar Primero)

- ⚠️ Cambiar nombres de tablas o columnas después de crear migraciones
- ⚠️ Agregar campos adicionales no definidos en PROJECT.md
- ⚠️ Modificar relaciones después de que estén implementadas
- ⚠️ Cambiar tipos de datos de campos existentes
- ⚠️ Agregar índices adicionales no especificados
- ⚠️ Modificar la estructura de seeds después de crearlos

### Never (Nunca)

- ❌ Implementar lógica de negocio en los modelos (solo datos y relaciones)
- ❌ Hardcodear valores de negocio (usar constantes o configuración)
- ❌ Crear migraciones manuales (siempre usar `flask db migrate`)
- ❌ Modificar migraciones ya aplicadas (crear nuevas migraciones)
- ❌ Omitir campos de auditoría en cualquier entidad
- ❌ Usar enums nativos de MySQL (usar strings para flexibilidad)
- ❌ Implementar soft delete complejo (solo campo `activo` booleano)
- ❌ Crear dependencias circulares entre modelos
- ❌ Omitir tests unitarios para modelos

---

## Success Criteria

### Criterios Funcionales

- [ ] Las 8 entidades del PROJECT.md están implementadas como modelos SQLAlchemy:
  - [ ] Municipio
  - [ ] ColoniaComunidad
  - [ ] Cobertura
  - [ ] Plan
  - [ ] DisponibilidadPlanZona
  - [ ] SolicitudInstalacion
  - [ ] NotaSolicitud
  - [ ] UsuarioAdministrativo

- [ ] Todos los campos definidos en PROJECT.md están presentes en cada modelo
- [ ] Todas las relaciones están correctamente definidas y probadas
- [ ] Los campos de auditoría están en todas las entidades (creado_por y actualizado_por son FK nullable a UsuarioAdministrativo)
- [ ] Los constraints (unique, not null, foreign key) están implementados
- [ ] Los índices están creados para campos de búsqueda frecuente
- [ ] El campo `reglas` en Cobertura usa tipo JSON compatible con MySQL y SQLite

### Criterios de Migraciones

- [ ] Las migraciones son ejecutables con `flask db upgrade`
- [ ] Las migraciones son reversibles con `flask db downgrade`
- [ ] El esquema resultante coincide exactamente con los modelos
- [ ] No hay errores de integridad referencial

### Criterios de Seeds

- [ ] Los seeds crean datos válidos y realistas
- [ ] Los seeds son ejecutables con `flask seed` (comando CLI personalizado) o `python seeds/initial_data.py`
- [ ] Los datos de prueba permiten probar todos los casos de uso
- [ ] Los seeds incluyen al menos:
  - [ ] 3-5 municipios reales de Guerrero (Acapulco, Chilpancingo, Iguala, Taxco, Zihuatanejo)
  - [ ] 5-10 colonias/comunidades reales de esos municipios
  - [ ] 3 planes de internet genéricos (Básico 20Mbps, Estándar 50Mbps, Premium 100Mbps)
  - [ ] 1 usuario administrador (admin@example.com)
  - [ ] 1-2 coberturas de ejemplo
  - [ ] 1-2 solicitudes de ejemplo

### Criterios de Testing

- [ ] Tests unitarios existen para cada modelo
- [ ] Tests verifican creación de instancias
- [ ] Tests verifican relaciones entre modelos
- [ ] Tests verifican constraints y validaciones
- [ ] Tests verifican manejo de JSON en campo reglas (compatible con SQLite y MySQL)
- [ ] Coverage de modelos es 90%+
- [ ] Todos los tests pasan con `pytest tests/models/`

### Criterios de Documentación

- [ ] Docstrings explican el propósito de cada modelo
- [ ] Docstrings explican las relaciones
- [ ] Docstrings explican el manejo de usuarios anónimos en campos de auditoría
- [ ] README de modelos explica la estructura
- [ ] Comentarios explican decisiones de diseño

---

## Open Questions

**Todas las preguntas abiertas han sido resueltas y documentadas en las secciones correspondientes:**

✅ **Versión de Python**: 3.14.6 (alineada con Fase 1)  
✅ **Convención de nombres**: Plural snake_case confirmado como regla oficial del proyecto  
✅ **Seeds**: Comando CLI personalizado `flask seed` implementado en `app/cli.py`  
✅ **JSON en SQLite**: Campo `reglas` usa `db.JSON` compatible con MySQL y SQLite  
✅ **Auditoría**: `creado_por` y `actualizado_por` son FK nullable a UsuarioAdministrativo (NULL para usuarios anónimos del portal)  
✅ **Seeds reales vs ficticios**: Datos reales de Guerrero (municipios y colonias) + planes genéricos  

---

## Decisions Made

### 1. Versión de Python
**Decisión**: Usar Python 3.14.6 (versión estable adoptada en Fase 1)  
**Justificación**: Mantener consistencia con la infraestructura ya configurada

### 2. Convención de Nombres
**Decisión**: Tablas en plural snake_case (regla oficial del proyecto)  
**Ejemplos**: `municipios`, `colonias_comunidades`, `solicitudes_instalacion`  
**Justificación**: Claridad y consistencia en todo el proyecto

### 3. Manejo de Seeds
**Decisión**: Implementar comando CLI personalizado `flask seed`  
**Implementación**: 
- Archivo: `app/cli.py` con función `register_commands(app)`
- Alternativa: `python seeds/initial_data.py`
**Justificación**: Flask no incluye comando `seed` por defecto

### 4. JSON en SQLite/Testing
**Decisión**: Usar `db.JSON` que SQLAlchemy adapta automáticamente  
**Comportamiento**:
- MySQL: JSON nativo
- SQLite: TEXT con serialización JSON automática
**Justificación**: Compatibilidad transparente entre entornos

### 5. Auditoría para Usuarios Anónimos
**Decisión**: `creado_por` y `actualizado_por` son FK nullable a UsuarioAdministrativo  
**Comportamiento**:
- Solicitudes del portal: `creado_por=NULL`
- Solicitudes de administradores: `creado_por=usuario_id`
**Justificación**: Permite distinguir registros del sistema vs usuarios

### 6. Seeds Reales vs Ficticios
**Decisión**: Usar datos reales de Guerrero + planes genéricos  
**Datos reales**:
- Municipios: Acapulco, Chilpancingo, Iguala, Taxco, Zihuatanejo
- Colonias: Colonias reales de esos municipios
**Datos genéricos**:
- Planes: Básico 20Mbps, Estándar 50Mbps, Premium 100Mbps
**Justificación**: Datos realistas para testing sin problemas de privacidad

### 7. Campo `estado` en Municipio
**Decisión**: String para estado de la república (ej: "Guerrero")  
**Justificación**: El PROJECT.md define `estado` como campo geográfico, no estado interno

### 8. Campo `tipo` en ColoniaComunidad
**Decisión**: String simple (no enum nativo de MySQL)  
**Valores**: 'colonia', 'comunidad', 'ranchería', 'otra'  
**Justificación**: Flexibilidad y compatibilidad con SQLite

### 9. Campo `ultimo_acceso` en Usuario
**Decisión**: Se actualiza en cada login  
**Justificación**: Balance entre información útil y overhead de BD

### 10. Índices
**Decisión**: Índices en FKs y campos de búsqueda frecuente  
**Índices compuestos**:
- `idx_solicitud_estado_fecha` (estado, fecha_creacion)
- `idx_solicitud_municipio_colonia` (municipio_id, colonia_id)
**Justificación**: Optimizar consultas más comunes

---

## Risks and Mitigations

### Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Migraciones fallan en MySQL | MEDIA | ALTO | Probar migraciones en MySQL local antes de commit |
| Relaciones circulares entre modelos | BAJA | ALTO | Usar `backref` en lugar de `back_populates` cuando sea posible |
| Seeds fallan por constraints | MEDIA | MEDIO | Crear seeds en orden correcto (primero entidades sin FK) |
| Tests lentos por creación de BD | BAJA | BAJO | Usar SQLite en memoria para tests (ya configurado) |
| Campos JSON no soportados en SQLite | BAJA | MEDIO | Usar tipo Text para JSON en testing, JSON en MySQL |

### Riesgos de Diseño

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Modelo no soporta casos de uso futuros | MEDIA | ALTO | Revisar PROJECT.md cuidadosamente, agregar campos de expansión |
| Relaciones incorrectas | BAJA | ALTO | Validar relaciones con tests unitarios exhaustivos |
| Índices insuficientes | MEDIA | MEDIO | Agregar índices para todos los FKs y campos de búsqueda |
| Seeds no realistas | BAJA | BAJO | Usar datos reales de Guerrero y planes genéricos realistas |

### Mitigaciones Generales

1. **Revisión de PROJECT.md**: Leer cuidadosamente el modelo de datos conceptual antes de implementar
2. **Tests exhaustivos**: Escribir tests para cada modelo, relación y constraint
3. **Migraciones incrementales**: Crear migraciones pequeñas y verificables
4. **Documentación**: Documentar decisiones de diseño en docstrings
5. **Validación manual**: Verificar esquema resultante con `SHOW CREATE TABLE` en MySQL

---

## Dependencies

### Dependencias Internas

- ✅ Fase 1 completada (infraestructura base)
- ✅ Flask-SQLAlchemy configurado
- ✅ Flask-Migrate inicializado
- ✅ pytest configurado

### Dependencias Externas

- MySQL 8.0+ (desarrollo)
- SQLite (testing, ya incluido en Python)

---

## Deliverables

### Código

- [ ] `app/models/base.py` - Clase base con campos de auditoría
- [ ] `app/models/municipio.py` - Modelo Municipio
- [ ] `app/models/colonia.py` - Modelo ColoniaComunidad
- [ ] `app/models/cobertura.py` - Modelo Cobertura
- [ ] `app/models/plan.py` - Modelo Plan
- [ ] `app/models/disponibilidad_plan.py` - Modelo DisponibilidadPlanZona
- [ ] `app/models/solicitud.py` - Modelo SolicitudInstalacion
- [ ] `app/models/nota_solicitud.py` - Modelo NotaSolicitud
- [ ] `app/models/usuario.py` - Modelo UsuarioAdministrativo
- [ ] `app/models/__init__.py` - Exportar todos los modelos

### Migraciones

- [ ] Migración inicial con todas las tablas
- [ ] Migraciones ejecutables y reversibles
- [ ] Schema validado en MySQL

### Seeds

- [ ] `seeds/initial_data.py` - Script de seeds
- [ ] Datos de prueba realistas
- [ ] Comando `flask seed` funcional

### Tests

- [ ] `tests/models/test_municipio.py`
- [ ] `tests/models/test_colonia.py`
- [ ] `tests/models/test_cobertura.py`
- [ ] `tests/models/test_plan.py`
- [ ] `tests/models/test_disponibilidad_plan.py`
- [ ] `tests/models/test_solicitud.py`
- [ ] `tests/models/test_nota_solicitud.py`
- [ ] `tests/models/test_usuario.py`
- [ ] `tests/models/test_relaciones.py`
- [ ] `tests/models/test_constraints.py`

### Documentación

- [ ] Docstrings en todos los modelos
- [ ] README de modelos explicando estructura
- [ ] Comentarios en decisiones de diseño

---

## Timeline Estimado

- **Día 1**: Implementar clase base y primeros 3 modelos (Municipio, Colonia, Cobertura)
- **Día 2**: Implementar modelos restantes (Plan, DisponibilidadPlan, Solicitud, Nota, Usuario)
- **Día 3**: Crear migración inicial y validar schema
- **Día 4**: Implementar seeds y validar datos
- **Día 5**: Escribir tests unitarios y validar coverage
- **Día 6**: Documentación y revisión final

**Total estimado**: 6 días de trabajo

---

## Approval Checklist

Antes de comenzar la implementación, confirmar:

- [ ] Especificación revisada y entendida
- [ ] Suposiciones validadas o corregidas
- [ ] Preguntas abiertas resueltas
- [ ] Estructura de archivos clara
- [ ] Estrategia de testing definida
- [ ] Criterios de éxito específicos y medibles
- [ ] Riesgos identificados y mitigaciones planificadas
- [ ] Timeline realista

---

**Estado**: ✅ ESPECIFICACIÓN CERRADA Y LISTA PARA IMPLEMENTACIÓN

**Próximo paso**: Proceder con implementación incremental de modelos, migraciones, seeds y tests.
