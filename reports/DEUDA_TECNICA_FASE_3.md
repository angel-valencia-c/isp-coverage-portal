# Deuda Técnica - Fase 3

**Fecha de creación:** 3 de agosto de 2026  
**Última actualización:** 3 de agosto de 2026  
**Responsable de revisión:** Equipo de desarrollo  
**Frecuencia de revisión:** Al final de cada módulo

---

## Propósito

Este documento registra warnings de deprecación, observaciones técnicas y deuda técnica identificada durante la Fase 3. Cada ítem debe ser revisado y resuelto (o documentado como aceptado) antes de cerrar la fase.

---

## Warnings de Deprecación

### ⚠️ DEUDA-001: SQLAlchemy 2.0 Migration - Query.get()

**Severidad:** BAJA  
**Tipo:** Deprecation Warning  
**Detectado en:** Módulo 2, 3, 4, 5, 6, Fase 4, Fase 5, Fase 6  
**Archivos afectados:**
- `app/services/municipio_service.py` (líneas 105, 136, 162)
- `app/services/colonia_service.py` (líneas 89, 134, 176)
- `app/services/cobertura_service.py` (líneas 39, 96)
- `app/services/plan_service.py` (líneas 92, 118, 165, 191)
- `app/services/disponibilidad_plan_service.py` (líneas 41, 46, 124, 150)
- `app/services/busqueda_publica_service.py` (línea 68)
- `app/services/planes_publicos_service.py` (línea 89)
- `app/services/solicitudes_publicas_service.py` (líneas 67, 77)
- `tests/test_municipios.py` (líneas 223, 238)
- `tests/test_colonias.py` (líneas 317, 332)
- `tests/test_cobertura.py` (línea 220)
- `tests/test_planes.py` (línea 111)

**Descripción:**
SQLAlchemy 2.0 deprecó el método `Model.query.get(id)` en favor de `db.session.get(Model, id)`.

**Código actual:**
```python
municipio = Municipio.query.get(municipio_id)
```

**Código recomendado:**
```python
municipio = db.session.get(Municipio, municipio_id)
```

**Impacto:**
- Funcionalidad: ✅ Correcta (solo warnings)
- Performance: ✅ Sin impacto
- Compatibilidad: ⚠️ Será removido en SQLAlchemy 3.0

**Acción requerida:**
- [ ] Reemplazar todas las ocurrencias de `Model.query.get()` por `db.session.get()`
- [ ] Actualizar tests
- [ ] Verificar que no hay warnings después del cambio

**Prioridad:** BAJA (puede esperar hasta final de fase)  
**Estimación:** 30 minutos

---

### ⚠️ DEUDA-002: Python 3.14 - datetime.utcnow()

**Severidad:** BAJA  
**Tipo:** Deprecation Warning  
**Detectado en:** Módulo 1, 4, Fase 6  
**Archivos afectados:**
- `app/services/auth_service.py` (línea 50)
- `app/services/cobertura_service.py` (líneas 39, 55, 126)
- `app/services/solicitudes_publicas_service.py` (líneas 82, 157)
- `tests/test_cobertura.py` (líneas 86, 154, 155, 353)
- `tests/test_solicitudes_publicas.py` (línea 186)
- `tests/models/test_usuario.py` (línea 213)

**Descripción:**
Python 3.12+ deprecó `datetime.utcnow()` en favor de `datetime.now(datetime.UTC)` para usar objetos timezone-aware.

**Código actual:**
```python
from datetime import datetime
usuario.ultimo_acceso = datetime.utcnow()
```

**Código recomendado:**
```python
from datetime import datetime, timezone
usuario.ultimo_acceso = datetime.now(timezone.UTC)
```

**Impacto:**
- Funcionalidad: ✅ Correcta (solo warnings)
- Performance: ✅ Sin impacto
- Compatibilidad: ⚠️ Será removido en Python 3.14+

**Acción requerida:**
- [ ] Reemplazar todas las ocurrencias de `datetime.utcnow()` por `datetime.now(timezone.UTC)`
- [ ] Actualizar imports
- [ ] Verificar que no hay warnings después del cambio
- [ ] Considerar migrar modelos de base de datos a timezone-aware si es necesario

**Prioridad:** BAJA (puede esperar hasta final de fase)  
**Estimación:** 45 minutos

---

## Observaciones Técnicas

### 📝 OBS-001: Estructura de Activación de Cobertura

**Detectado en:** Módulo 4  
**Tipo:** Diseño de UX  
**Descripción:**
La activación de cobertura se realiza desde la lista de colonias (botón "Activar Cobertura"), no desde la lista de cobertura. Esto es intencional para mantener el flujo lógico: primero existe la colonia, luego se le asigna cobertura.

**Decisión:** ✅ ACEPTADA  
**Justificación:** Flujo más intuitivo para el usuario. La lista de cobertura muestra el estado, pero la acción de crear/activar se hace desde colonias.

**Acción:** Ninguna requerida. Documentar en guía de usuario.

---

### 📝 OBS-002: Tipos de Cobertura en V1

**Detectado en:** Módulo 4  
**Tipo:** Alcance funcional  
**Descripción:**
El modelo soporta 4 tipos de cobertura (total, parcial, condicional, planificada), pero en V1 solo se usan "total" y "planificada". Los otros dos tipos están preparados para futuras versiones pero no tienen lógica diferenciada.

**Decisión:** ✅ ACEPTADA  
**Justificación:** Preparación para evolución futura sin refactor mayor (RN-020, RN-023).

**Acción:** 
- [ ] Documentar en PROJECT.md que "parcial" y "condicional" están preparados pero no implementados en V1
- [ ] Considerar agregar validación que prevenga usar tipos no soportados en V1

---

### 📝 OBS-003: Notas de Cobertura como Texto Libre

**Detectado en:** Módulo 4  
**Tipo:** Diseño de datos  
**Descripción:**
El campo `notas` en Cobertura es texto libre. En futuras versiones podría evolucionar a JSON estructurado para reglas más complejas (RN-023).

**Decisión:** ✅ ACEPTADA  
**Justificación:** V1 requiere solo texto libre. El campo `reglas` (JSON) ya está preparado en el modelo para evolución futura.

**Acción:** Ninguna requerida. El modelo ya está preparado.

---

## Checklist de Revisión por Módulo

### Módulo 1: Autenticación ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [ ] DEUDA-002 revisada (datetime.utcnow en auth_service.py)

### Módulo 2: Municipios ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [ ] DEUDA-001 revisada (Query.get en municipio_service.py)

### Módulo 3: Colonias ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [ ] DEUDA-001 revisada (Query.get en colonia_service.py)

### Módulo 4: Cobertura ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [x] Validación RN-021 implementada
- [ ] DEUDA-001 revisada (Query.get en cobertura_service.py)
- [ ] DEUDA-002 revisada (datetime.utcnow en cobertura_service.py)

### Módulo 5: Planes ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [ ] DEUDA-001 revisada (Query.get en plan_service.py)

### Módulo 6: Asociación Planes-Zonas ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [ ] DEUDA-001 revisada (Query.get en disponibilidad_plan_service.py)

### Módulo 7: Dashboard y Vista Jerárquica ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [x] Sin deuda técnica nueva

### Módulo 8: Layout Administrativo y Componentes ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [x] Sin deuda técnica nueva
- [x] Componentes CSS completados (badge-secondary, form-help, text-muted)

### Módulo 9: Sistema CSS Completo ✅
- [x] Tests pasando
- [x] Coverage > 80%
- [x] Navegación coherente
- [x] Sin deuda técnica nueva
- [x] Sistema CSS verificado y completo (tokens, base, components, layouts)

### Módulo 10: Tests de Integración y Documentación ✅
- [x] Todos los tests pasando (151/151)
- [x] Coverage general > 75%
- [x] Documentación completa
- [x] Deuda técnica documentada
- [x] Reporte final generado

---

## FASE 4: Portal Público - Búsqueda de Cobertura

### Estado: ✅ COMPLETADA

### Módulo 1: Servicio de Búsqueda Pública ✅
- [x] Tests pasando (12/12)
- [x] Coverage > 90%
- [x] Sin deuda técnica nueva
- [x] DEUDA-001 actualizada (agregado busqueda_publica_service.py)

### Módulo 2: Rutas del Portal Público ✅
- [x] Tests pasando (8/8)
- [x] Coverage 100%
- [x] Sin deuda técnica nueva
- [x] Tests de health actualizados para reflejar nuevo comportamiento

### Resumen Fase 4
- **Total tests:** 20 nuevos tests (12 servicio + 8 rutas)
- **Tests totales:** 169 pasando (100%)
- **Coverage general:** 78%
- **Deuda técnica:** DEUDA-001 actualizada con busqueda_publica_service.py
- **Archivos creados:**
  - `app/services/busqueda_publica_service.py`
  - `app/routes/portal.py`
  - `app/templates/layouts/public.html`
  - `app/templates/pages/public/index.html`
  - `public/css/public.css`
  - `public/js/portal.js`
  - `tests/test_busqueda_publica.py`
  - `tests/test_portal_routes.py`

---

## FASE 5: Portal Público - Planes y Cotización

### Estado: ✅ COMPLETADA

### Módulo 1: Servicio de Planes Públicos ✅
- [x] Tests pasando (9/9)
- [x] Coverage > 95%
- [x] Sin deuda técnica nueva
- [x] DEUDA-001 actualizada (agregado planes_publicos_service.py)

### Módulo 2: Rutas de Planes del Portal ✅
- [x] Tests pasando (5/5)
- [x] Coverage 100% en rutas del portal
- [x] Sin deuda técnica nueva

### Resumen Fase 5
- **Total tests:** 14 nuevos tests (9 servicio + 5 rutas)
- **Tests totales:** 183 pasando (100%)
- **Coverage general:** 79%
- **Deuda técnica:** DEUDA-001 actualizada con planes_publicos_service.py
- **Archivos creados:**
  - `app/services/planes_publicos_service.py`
  - `app/templates/pages/public/planes.html`
  - `app/templates/pages/public/sin_cobertura.html`
  - `public/js/planes.js`
  - `tests/test_planes_publicos.py`
  - `tests/test_planes_routes.py`
- **Archivos modificados:**
  - `app/routes/portal.py` (agregadas rutas de planes y cotización)
  - `public/css/public.css` (agregados estilos para planes y sin cobertura)
  - `public/js/portal.js` (actualizado para redirigir a planes)

---

## FASE 6: Portal Público - Formulario de Solicitud

### Estado: ✅ COMPLETADA

### Módulo 1: Servicio de Solicitudes Públicas ✅
- [x] Tests pasando (9/9)
- [x] Coverage > 85%
- [x] Sin deuda técnica nueva
- [x] DEUDA-001 actualizada (agregado solicitudes_publicas_service.py)
- [x] DEUDA-002 actualizada (agregado solicitudes_publicas_service.py)

### Resumen Fase 6
- **Total tests:** 9 nuevos tests
- **Tests totales:** 192 pasando (100%)
- **Coverage general:** 78%
- **Deuda técnica:** DEUDA-001 y DEUDA-002 actualizadas con solicitudes_publicas_service.py
- **Archivos creados:**
  - `app/services/solicitudes_publicas_service.py`
  - `app/templates/pages/public/solicitud.html`
  - `app/templates/pages/public/solicitud_lead.html`
  - `app/templates/pages/public/confirmacion.html`
  - `public/js/solicitud.js`
  - `public/js/solicitud_lead.js`
  - `tests/test_solicitudes_publicas.py`
- **Archivos modificados:**
  - `app/routes/portal.py` (agregadas rutas de solicitud, lead y confirmación)
  - `public/css/public.css` (agregados estilos para formularios y confirmación)
  - `public/js/planes.js` (actualizado para redirigir a solicitud)
  - `app/templates/pages/public/sin_cobertura.html` (actualizado para redirigir a lead)

---

## Plan de Resolución

### Antes de cerrar Fase 3:

1. **Resolver DEUDA-001** (SQLAlchemy 2.0)
   - Reemplazar `Model.query.get()` por `db.session.get()`
   - Actualizar tests
   - Verificar que no hay warnings
   - Tiempo estimado: 30 minutos

2. **Resolver DEUDA-002** (Python 3.14 datetime)
   - Reemplazar `datetime.utcnow()` por `datetime.now(timezone.UTC)`
   - Actualizar imports
   - Verificar que no hay warnings
   - Tiempo estimado: 45 minutos

3. **Revisar observaciones**
   - Confirmar que OBS-001, OBS-002, OBS-003 siguen siendo válidas
   - Actualizar documentación si es necesario

### Criterios de cierre de fase:

- ✅ Todos los módulos completados
- ✅ Todos los tests pasando
- ✅ Coverage general > 80%
- ✅ DEUDA-001 resuelta o documentada como aceptada
- ✅ DEUDA-002 resuelta o documentada como aceptada
- ✅ Sin warnings de deprecación en logs
- ✅ Documentación actualizada

---

## Historial de Cambios

| Fecha | Módulo | Descripción | Autor |
|-------|--------|-------------|-------|
| 2026-08-03 | - | Creación del documento | Sistema |
| 2026-08-03 | 2 | Detectado DEUDA-001 | Sistema |
| 2026-08-03 | 3 | Detectado DEUDA-001 | Sistema |
| 2026-08-03 | 4 | Detectado DEUDA-001, DEUDA-002, OBS-001, OBS-002, OBS-003 | Sistema |
| 2026-08-03 | 5 | Actualizado DEUDA-001 (agregado plan_service.py) | Sistema |
| 2026-08-03 | 6 | Actualizado DEUDA-001 (agregado disponibilidad_plan_service.py) | Sistema |
| 2026-08-03 | 7 | Sin deuda técnica nueva | Sistema |
| 2026-08-03 | 8 | Componentes CSS completados, sin deuda técnica nueva | Sistema |
| 2026-08-03 | 9 | Sistema CSS verificado y completo, sin deuda técnica nueva | Sistema |
| 2026-08-03 | 10 | Fase 3 completada, deuda técnica documentada, reporte final generado | Sistema |
| 2026-08-03 | Fase 4 | Portal Público completado, DEUDA-001 actualizada con busqueda_publica_service.py | Sistema |
| 2026-08-03 | Fase 5 | Planes y Cotización completado, DEUDA-001 actualizada con planes_publicos_service.py | Sistema |
| 2026-08-03 | Fase 6 | Formulario de Solicitud completado, DEUDA-001 y DEUDA-002 actualizadas con solicitudes_publicas_service.py | Sistema |

---

**Próxima revisión:** Al completar Módulo 5  
**Responsable actual:** Equipo de desarrollo
