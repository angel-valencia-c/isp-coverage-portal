# Portal de Verificación de Cobertura y Solicitud de Instalación

## Resumen Ejecutivo

Portal web para Internet Regional que permite a prospectos verificar disponibilidad de cobertura de internet en su ubicación, consultar planes disponibles, obtener una cotización estimada y solicitar instalación. El sistema incluye un panel administrativo para que el equipo de ventas gestione las solicitudes recibidas y un módulo de administración de catálogo de cobertura.

El producto reduce la carga operativa de atención telefónica, acelera el proceso de conversión de prospectos y proporciona visibilidad sobre la demanda de instalación por zona geográfica.

**Contexto de uso**: El portal debe funcionar óptimamente desde dispositivos móviles y desktop, incluyendo acceso desde códigos QR en carretera. La experiencia debe transmitir profesionalismo, confianza y facilitar la conversión comercial.

---

## Objetivo

Implementar un portal web que permita a los prospectos:

1. Verificar de forma autónoma si su ubicación tiene cobertura disponible.
2. Consultar los planes de internet disponibles en su zona.
3. Obtener una cotización estimada del servicio.
4. Solicitar la instalación del servicio mediante un formulario estructurado.

El sistema debe proporcionar al equipo de ventas una herramienta para visualizar y gestionar las solicitudes pendientes de contacto, y al superadministrador una interfaz para administrar el catálogo de cobertura, zonas y planes disponibles.

**Objetivo comercial**: Reducir la carga operativa de atención telefónica, acelerar el tiempo de conversión de prospectos y proporcionar visibilidad sobre demanda de instalación por zona geográfica.

**Objetivo técnico**: Implementar sistema modular, escalable y mantenible basado en catálogo estructurado, jerarquía territorial y reglas por área, preparado para evolución futura sin refactor mayor.

---

## Branding Base

### Identidad Corporativa

El proyecto pertenece a **Internet Regional**, empresa proveedora de servicios de internet. Todo el diseño visual, la comunicación y la experiencia de usuario deben reflejar la identidad de esta marca.

### Dirección Visual

**Principios de diseño**:
- **Profesionalismo**: Transmitir seriedad y confianza en el servicio.
- **Comercial**: Orientado a conversión y venta de servicios.
- **Telecomunicaciones**: Estética alineada con el sector (velocidad, conectividad, tecnología).
- **Accesible**: Diseño inclusivo que funcione para usuarios no técnicos.

**Paleta de colores base**:
- Se partirá de los colores corporativos de Internet Regional.
- El agente de frontend propondrá la paleta final basada en la identidad de marca.
- Los colores deben transmitir: confianza, tecnología, velocidad y profesionalismo.
- Se recomienda incluir colores de acento para llamadas a la acción (CTAs).

**Tipografía**:
- El agente de frontend seleccionará tipografías que complementen la identidad de marca.
- Deben ser legibles en dispositivos móviles y desktop.
- Se recomienda usar máximo 2 familias tipográficas (una para títulos, otra para cuerpo).

**Estilo visual**:
- Diseño limpio y moderno, sin sobrecarga visual.
- Jerarquía clara de información (lo importante primero).
- Uso consistente de espaciados, bordes y sombras.
- Imágenes o iconografía de alta calidad relacionadas con conectividad e internet.
- Botones y elementos interactivos con estados claros (hover, active, disabled).

**Tono de comunicación**:
- Cercano pero profesional.
- Orientado a la acción y beneficios para el usuario.
- Mensajes claros y sin jerga técnica innecesaria.
- En español mexicano.

### Activos de Marca

**Pendiente de definir**:
- Logo de Internet Regional y sus variantes (horizontal, vertical, ícono).
- Manual de marca o lineamientos de branding específicos.
- Imágenes o fotografías oficiales de la empresa.

**Recomendación**: Solicitar al cliente los activos de marca disponibles antes de iniciar el diseño visual final. Si no existen lineamientos formales, el agente de frontend propondrá una dirección visual coherente con el sector de telecomunicaciones.

---

## Stack Tecnológico Base

### Frontend

**Tecnologías principales**:
- **HTML5**: Estructura semántica y accesible.
- **CSS3**: Estilos responsivos con Flexbox y Grid.
- **JavaScript (ES6+)**: Interactividad y lógica de cliente.

**Enfoque**:
- Implementación sin frameworks pesados en V1 para mantener simplicidad y control total.
- Código vanilla JavaScript para máxima compatibilidad y rendimiento.
- Estructura modular que permita evolución futura hacia frameworks si es necesario.
- Componentes reutilizables para mantener consistencia visual.

**Responsividad**:
- Diseño mobile-first con breakpoints para tablet y desktop.
- Pruebas en dispositivos reales y emuladores.
- Optimización para conexiones lentas (3G/4G).

### Backend

**Tecnologías sugeridas** (a definir según necesidades específicas):
- **Node.js con Express**: Para API REST y lógica de servidor.
- **Base de datos**: PostgreSQL o MySQL para datos relacionales estructurados.
- **Autenticación**: JWT o sesiones seguras para panel administrativo.

**Alternativas consideradas**:
- PHP con Laravel: Viable si el equipo tiene experiencia previa.
- Python con Flask/Django: Viable si se requiere procesamiento adicional.

**Decisión final**: El stack backend específico será definido durante la fase de arquitectura técnica, considerando:
- Experiencia del equipo de desarrollo.
- Facilidad de despliegue y mantenimiento.
- Escalabilidad futura.
- Integración con infraestructura existente.

### Herramientas de Desarrollo

**Gestión de dependencias**:
- npm o yarn para paquetes de frontend.
- Paquetes backend según stack seleccionado.

**Control de versiones**:
- Git para control de código fuente.
- Estructura de ramas clara (main, develop, feature branches).

**Despliegue**:
- Servidor web (Apache, Nginx o similar).
- Base de datos relacional.
- Variables de entorno para configuración.

---

## Arquitectura

### Principios de Diseño

**Arquitectura por capas**:
El sistema debe organizarse en capas claramente separadas con responsabilidades definidas:

1. **Capa de Presentación**:
   - Componentes visuales (HTML, CSS).
   - Lógica de interacción de usuario (JavaScript de cliente).
   - Validaciones de formulario.
   - Renderizado de datos.

2. **Capa de Aplicación**:
   - Controladores de rutas.
   - Lógica de flujo de aplicación.
   - Orquestación de casos de uso.
   - Manejo de solicitudes HTTP.

3. **Capa de Dominio**:
   - Entidades de negocio.
   - Reglas de negocio.
   - Lógica de validación compleja.
   - Servicios de dominio.

4. **Capa de Persistencia/Infraestructura**:
   - Acceso a base de datos.
   - Repositorios.
   - Servicios externos (si aplica).
   - Configuración de infraestructura.

**Principio de Responsabilidad Única (SRP)**:
- Cada módulo, archivo o componente debe tener una sola razón para cambiar.
- Evitar que una sola pieza de código haga demasiadas cosas.
- Separar claramente:
  - Lógica de presentación de lógica de negocio.
  - Lógica de negocio de acceso a datos.
  - Configuración de implementación.

**Modularidad**:
- Estructura de carpetas organizada por funcionalidad o módulo.
- Componentes reutilizables donde tenga sentido.
- Dependencias explícitas entre módulos.
- Interfaces claras entre capas.

### Estructura de Carpetas Sugerida

```
/proyecto
├── /public                 # Archivos estáticos accesibles públicamente
│   ├── /css               # Estilos globales y de componentes
│   ├── /js                # JavaScript de cliente
│   ├── /images            # Imágenes y activos visuales
│   └── /fonts             # Tipografías personalizadas
├── /src                   # Código fuente de la aplicación
│   ├── /controllers       # Controladores de rutas
│   ├── /services          # Lógica de aplicación y servicios
│   ├── /models            # Modelos de datos y acceso a BD
│   ├── /views             # Plantillas HTML (si aplica server-side rendering)
│   ├── /middleware        # Middleware de autenticación, validación, etc.
│   ├── /utils             # Utilidades y funciones auxiliares
│   └── /config            # Configuración de la aplicación
├── /database              # Migraciones y seeds de base de datos
├── /tests                 # Pruebas unitarias y de integración
└── /docs                  # Documentación adicional
```

**Nota**: Esta estructura es una sugerencia inicial. El agente de arquitectura técnica puede ajustarla según el stack backend seleccionado y las necesidades específicas del proyecto.

### Separación de Responsabilidades

**Vista Pública**:
- Módulo independiente con sus propios componentes, estilos y lógica.
- No debe tener dependencias directas con la vista administrativa.
- Puede compartir servicios y modelos con otras capas.

**Vista Administrativa**:
- Módulo independiente con autenticación obligatoria.
- Separado visual y funcionalmente de la vista pública.
- Puede compartir modelos y servicios con la vista pública.

**Gestión de Cobertura**:
- Módulo administrativo especializado.
- Acceso restringido a superadministradores.
- Lógica de negocio específica para administración de zonas y planes.

### Escalabilidad

**Preparado para crecer**:
- La arquitectura debe permitir agregar nuevos módulos sin refactor mayor.
- Las capas deben poder evolucionar independientemente.
- El código debe ser testeable y mantenible.

---

## Alcance de la Primera Versión (V1)

### Incluido en V1

**Vista Pública (Prospectos)**:
- Landing page con buscador de ubicación destacado.
- Selector cascada de ubicación: Municipio → Colonia/Comunidad con búsqueda.
- Visualización de disponibilidad de cobertura para la ubicación consultada.
- Listado de planes disponibles según la zona (tipo pricing table).
- Cotización estimada basada en el plan seleccionado y ubicación (costo estándar base + ajuste por zona).
- Formulario de solicitud de instalación con datos de contacto.
- Flujo alternativo para dejar datos cuando no hay cobertura.
- Mensaje de confirmación después de envío exitoso.
- Aviso claro de que la cotización es estimada y sujeta a validación.
- Aviso claro de que la contratación formal requiere contrato firmado.

**Vista Administrativa (Equipo de Ventas)**:
- Login con autenticación segura.
- Dashboard con tabla de solicitudes.
- Filtros por estado (pendiente, contactado, agendado, cancelado, duplicado).
- Vista de detalles de solicitud en modal o panel lateral.
- Capacidad de cambiar estado de solicitudes.
- Sistema de notas internas con historial (múltiples notas por solicitud).
- Vista de mapeo básico (tabla agrupada por municipio/colonia con conteos).
- Exportación de solicitudes a CSV/Excel.

**Gestión de Cobertura (Superadministrador)**:
- Administración del catálogo de municipios, colonias y comunidades.
- Asociación de cobertura a ubicaciones específicas.
- Configuración de planes disponibles por zona.
- Configuración de costo de instalación por zona o plan.
- Activación/desactivación de cobertura por zona.

**Funcionalidades Transversales**:
- Validación de duplicados básica (mismo teléfono en últimos 7 días).
- Campos de auditoría en entidades principales (creado_por, fecha_creación, etc.).
- Diseño responsivo mobile-first.
- Protección contra ataques comunes (SQL injection, XSS, CSRF).

### No Incluido en V1

- Mapas interactivos con GIS o coordenadas geográficas complejas.
- Pagos en línea o integración con sistemas de facturación.
- Agendamiento automático de instalaciones con calendario.
- Cuentas de usuario para prospectos (login/registro).
- Integración con sistemas de provisión técnica.
- Notificaciones automáticas por correo o SMS.
- Reportes avanzados o dashboards analíticos complejos.
- Sistema de tickets o soporte al cliente.
- Validación técnica automática de factibilidad de instalación.
- Multi-idioma (solo español).
- Aplicación móvil nativa.
- Integración con redes sociales o WhatsApp Business.

---

## Roles de Usuario

### 1. Prospecto (Usuario Público)

**Descripción**: Persona interesada en contratar el servicio de internet de Internet Regional. No requiere autenticación.

**Objetivos**:
- Saber si su ubicación tiene cobertura.
- Ver planes relacionados con su zona.
- Obtener cotización estimada.
- Solicitar la instalación del servicio.
- Si no tiene cobertura, dejar datos para seguimiento.

**Experiencia esperada en V1**:
- Acceso desde dispositivos móviles y desktop, incluyendo QR en carretera.
- No requiere registro ni login.
- Interacción limitada a consulta y solicitud.
- Experiencia visual comercial y confiable tipo telecom.
- Proceso rápido: verificación de cobertura en menos de 10 segundos.
- Formularios intuitivos con validación en tiempo real.
- Mensajes claros y orientados a la acción.

### 2. Superadministrador

**Descripción**: Usuario con permisos completos del sistema. Responsable de administrar el catálogo de cobertura, planes, costos, usuarios administrativos y la delimitación territorial del servicio. **Es el usuario más importante para la gestión territorial del sistema.**

**Objetivos**:
- Administrar catálogo de municipios, colonias y comunidades.
- Definir qué zonas existen y cómo se organizan jerárquicamente.
- Delimitar cobertura por municipio, colonia, comunidad y futuras subdivisiones.
- Activar, desactivar, ampliar o reducir cobertura.
- Configurar reglas de disponibilidad por área.
- Asociar planes disponibles a cada zona.
- Configurar costos de instalación por zona o plan.
- Gestionar usuarios administrativos.

**Experiencia operativa en V1**:
- Interfaz clara y eficiente para administración de zonas y cobertura.
- Vista jerárquica del territorio: Municipio → Colonia/Comunidad → Cobertura.
- Capacidad de ver estado de cobertura por zona de un vistazo.
- Herramientas para activar/desactivar cobertura rápidamente.
- Configuración intuitiva de planes y costos por zona.
- Validaciones que prevengan errores comunes (ej: desactivar zona con solicitudes pendientes).
- Feedback visual claro sobre acciones realizadas.

**Permisos**:
- Acceso total a todas las funcionalidades del sistema.
- Gestión de catálogo de cobertura y zonas.
- Gestión de usuarios administrativos.
- Visualización y gestión de todas las solicitudes.
- Configuración de reglas de negocio por zona.

### 3. Administrador / Personal de Ventas

**Descripción**: Miembro del equipo de Internet Regional encargado de gestionar las solicitudes de instalación recibidas y dar seguimiento a prospectos.

**Objetivos**:
- Ver solicitudes agrupadas por zona.
- Entender dónde hay más demanda.
- Priorizar llamadas y seguimiento.
- Detectar zonas con mayor interés comercial.
- Contactar a los prospectos para agendar instalación.
- Actualizar el estado de las solicitudes.
- Agregar notas internas de seguimiento.

**Experiencia operativa en V1**:
- Dashboard con solicitudes agrupadas por zona para identificar concentración geográfica.
- Vista de mapeo básico (tabla agrupada por municipio/colonia con conteos).
- Filtros por estado, zona y fecha para priorizar trabajo.
- Capacidad de ver tendencias básicas (ej: "esta semana hubo 15 solicitudes en X colonia").
- Interfaz eficiente para gestión de múltiples solicitudes.
- Notas internas con historial completo para seguimiento.
- Exportación de datos para análisis externo si es necesario.

**Permisos**:
- Visualización de solicitudes.
- Cambio de estado de solicitudes.
- Agregado de notas internas.
- Exportación de datos.
- Visualización de análisis básico de demanda por zona.
- **No puede** modificar catálogo de cobertura, zonas ni gestionar usuarios.

**Nota**: En V1, los roles de "Administrador" y "Personal de Ventas" pueden combinarse en un solo rol con permisos de gestión de solicitudes.

---

## Política de Costos y Contratación

### Estructura de Costos

**Costo estándar base**:
- El superadministrador define un costo estándar base de instalación aplicable a todas las zonas.
- Este costo base puede ajustarse por zona específica según complejidad, distancia o infraestructura disponible.

**Cálculo de cotización**:
- La cotización mostrada al prospecto = costo estándar base + ajuste por zona (si existe) + mensualidad del plan.
- La cotización es **estimada** y puede variar después de validación técnica.

### Proceso de Contratación

1. Prospecto verifica cobertura y obtiene cotización estimada.
2. Prospecto envía solicitud de instalación.
3. Equipo de ventas contacta al prospecto.
4. Se valida factibilidad técnica y se confirma costo final.
5. Se firma contrato de servicio (fuera del portal).
6. Se agenda y ejecuta instalación.

### Fuera del Alcance en V1

- Gestión electrónica de firma de contratos.
- Generación automática de documentos contractuales.
- Almacenamiento de contratos firmados en el sistema.
- Flujo de aprobación de contratos.
- Integración con sistemas de gestión documental.

---

## Requisitos Funcionales

### Vista Pública

**RF-001**: El sistema debe permitir buscar ubicación por municipio mediante selector cascada con campo de búsqueda.

**RF-002**: El sistema debe permitir buscar ubicación por colonia o comunidad dentro del municipio seleccionado, con autocompletado y búsqueda parcial.

**RF-003**: El sistema debe mostrar si hay cobertura disponible para la ubicación seleccionada.

**RF-004**: Si hay cobertura, el sistema debe mostrar los planes disponibles en esa zona en formato de tarjetas (pricing table).

**RF-005**: Cada plan debe mostrar: nombre del plan, velocidad de descarga, velocidad de subida y precio mensual.

**RF-006**: El sistema debe mostrar una cotización estimada que incluya: costo de instalación (costo estándar base + ajuste por zona, si aplica) y mensualidad del plan seleccionado. La cotización debe indicar claramente que es estimada y sujeta a validación técnica.

**RF-007**: El sistema debe proporcionar un formulario de solicitud con los siguientes campos obligatorios:
- Nombre completo del prospecto
- Número de teléfono de contacto (10 dígitos)
- Dirección específica (calle, número, referencias)
- Plan seleccionado (prellenado automáticamente)
- Ubicación (municipio, colonia/comunidad - prellenado automáticamente)

**RF-008**: El sistema debe validar que todos los campos obligatorios del formulario estén completos antes de permitir el envío.

**RF-009**: El sistema debe validar que el número de teléfono tenga formato válido (10 dígitos numéricos para México).

**RF-010**: Después del envío exitoso, el sistema debe mostrar un mensaje de confirmación al prospecto con número de solicitud.

**RF-011**: El sistema debe registrar la solicitud en la base de datos con estado "pendiente" y origen "portal".

**RF-012**: Si no hay cobertura en la ubicación consultada, el sistema debe ofrecer la opción de dejar datos de contacto (nombre y teléfono) para ser avisado cuando haya cobertura en esa zona.

**RF-013**: El sistema debe validar si existe otra solicitud pendiente con el mismo teléfono en los últimos 7 días. Si existe, mostrar mensaje: "Ya tienes una solicitud pendiente. Te contactaremos pronto."

**RF-014**: El sistema debe mostrar aviso visible de que la contratación formal requiere contrato firmado con Internet Regional.

### Vista Administrativa

**RF-015**: El sistema debe requerir autenticación (usuario y contraseña) para acceder al panel administrativo.

**RF-016**: El sistema debe mostrar una tabla con todas las solicitudes de instalación.

**RF-017**: La tabla debe mostrar: fecha de solicitud, nombre del prospecto, teléfono, ubicación (municipio y colonia), plan solicitado, origen y estado actual.

**RF-018**: El sistema debe permitir filtrar solicitudes por estado (pendiente, contactado, agendado, cancelado, duplicado).

**RF-019**: El sistema debe permitir ordenar solicitudes por fecha (más recientes primero por defecto).

**RF-020**: El sistema debe permitir al administrador hacer clic en una solicitud para ver detalles completos en modal o panel lateral.

**RF-021**: La vista de detalles debe mostrar toda la información de la solicitud incluyendo dirección específica, cotización y notas internas.

**RF-022**: El sistema debe permitir al administrador cambiar el estado de una solicitud.

**RF-023**: El sistema debe permitir al administrador agregar notas internas a una solicitud. Las notas deben registrarse con timestamp y usuario que las agregó.

**RF-024**: El sistema debe mostrar el historial completo de notas internas en orden cronológico.

**RF-025**: El sistema debe proporcionar una vista de mapeo básico que agrupe solicitudes por municipio o colonia y muestre conteo de solicitudes por zona y estado.

**RF-026**: El sistema debe permitir exportar la lista de solicitudes a formato CSV o Excel, respetando filtros aplicados.

**RF-027**: El sistema debe permitir marcar una solicitud como duplicada de otra solicitud existente.

**RF-028**: El sistema debe proporcionar análisis básico de demanda por zona: conteo de solicitudes por municipio y colonia, diferenciando entre solicitudes con cobertura y sin cobertura.

**RF-029**: El sistema debe permitir filtrar el análisis de demanda por rango de fechas y por estado de solicitud.

**RF-030**: El sistema debe mostrar indicadores visuales de zonas con alta demanda (ej: top 10 colonias con más solicitudes).

### Gestión de Cobertura

**RF-031**: El sistema debe permitir administrar el catálogo de municipios, colonias y comunidades (crear, editar, desactivar).

**RF-032**: El sistema debe permitir asociar cobertura a una ubicación específica (colonia o comunidad).

**RF-033**: El sistema debe permitir configurar qué planes están disponibles en cada zona con cobertura.

**RF-034**: El sistema debe permitir configurar el costo de instalación por zona o plan. El superadministrador define el costo estándar base y puede ajustarlo por zona.

**RF-035**: El sistema debe permitir activar o desactivar cobertura por zona.

**RF-036**: El sistema debe proporcionar una interfaz administrativa para gestionar el catálogo de cobertura y planes con vista jerárquica del territorio.

**RF-037**: El sistema debe permitir gestionar usuarios administrativos (crear, editar, desactivar).

**RF-038**: El sistema debe permitir al superadministrador ver el estado de cobertura por zona de un vistazo (activa/inactiva, planes disponibles).

**RF-039**: El sistema debe validar que no se desactive una zona con solicitudes pendientes activas sin confirmación explícita.

**RF-040**: El sistema debe permitir configurar el tipo de cobertura (total o planificada en V1) para preparar estructura futura.

**RF-041**: El sistema debe permitir agregar notas y reglas básicas por zona de cobertura (campo de texto libre en V1, JSON estructurado en versiones futuras).

---

## Requisitos No Funcionales

### Rendimiento

**RNF-001**: El tiempo de respuesta para consultas de cobertura no debe exceder 2 segundos en condiciones normales de carga.

**RNF-002**: El sistema debe soportar al menos 50 usuarios concurrentes sin degradación significativa del rendimiento.

**RNF-003**: La carga inicial de la página principal no debe exceder 3 segundos en conexiones 4G.

### Usabilidad

**RNF-004**: La vista pública debe ser responsiva y funcionar correctamente en dispositivos móviles (pantallas de 320px a 1440px de ancho).

**RNF-005**: El proceso de verificación de cobertura y solicitud debe completarse en máximo 5 clics para un usuario que conoce su ubicación.

**RNF-006**: La interfaz debe seguir principios de diseño limpio y visual, con jerarquía clara de información.

**RNF-007**: Los mensajes de error deben ser específicos y orientados a la acción (ej: "Por favor ingresa tu número de teléfono" en lugar de "Error en el formulario").

**RNF-008**: Los elementos interactivos deben tener estados visuales claros (hover, active, disabled, loading).

### Disponibilidad

**RNF-009**: El sistema debe estar disponible al menos 95% del tiempo en horario de 7:00 AM a 11:00 PM.

### Seguridad

**RNF-010**: Las credenciales de acceso al panel administrativo deben almacenarse de forma segura (hash de contraseñas con bcrypt o similar).

**RNF-011**: El sistema debe proteger contra ataques comunes (SQL injection, XSS, CSRF).

**RNF-012**: Las sesiones de administrador deben expirar después de 30 minutos de inactividad.

**RNF-013**: Todas las comunicaciones deben usar HTTPS.

### Mantenibilidad

**RNF-014**: El código debe estar estructurado en módulos claramente separados (vista pública, vista administrativa, gestión de cobertura).

**RNF-015**: El catálogo de cobertura debe ser fácilmente actualizable sin requerir cambios en el código.

**RNF-016**: El código debe seguir principios de responsabilidad única (SRP).

**RNF-017**: Las dependencias entre módulos deben ser explícitas y mínimas.

### Compatibilidad

**RNF-018**: El sistema debe funcionar en los navegadores más recientes de Chrome, Firefox, Safari y Edge.

**RNF-019**: El sistema debe ser compatible con dispositivos móviles iOS y Android.

### Accesibilidad

**RNF-020**: El sistema debe cumplir con estándares básicos de accesibilidad WCAG 2.1 nivel AA.

**RNF-021**: Los formularios deben ser navegables por teclado.

**RNF-022**: Los colores deben tener contraste suficiente para usuarios con dificultades visuales.

---

## Cobertura y Zonas

### Principios Fundamentales

**Separación de conceptos**:
- **Zona geográfica**: Entidad que representa una ubicación geográfica dentro de la jerarquía territorial. Es independiente de si hay servicio o no.
- **Cobertura**: Entidad que representa la disponibilidad de servicio en una zona geográfica específica. Incluye reglas, estado y configuración.

**Importante**: Zona geográfica y cobertura NO son lo mismo. Una zona puede existir sin cobertura (aún no hay servicio) o tener cobertura (servicio disponible). Esta separación permite:
- Mantener catálogo territorial completo aunque no todas las zonas tengan servicio.
- Activar/desactivar cobertura sin eliminar la zona del catálogo.
- Evolucionar hacia cobertura parcial o condicional sin romper la estructura territorial.
- Analizar demanda en zonas sin cobertura (leads para expansión).

### Jerarquía Territorial

**Estructura V1**:
```
Municipio
  └── Colonia/Comunidad
        └── Cobertura (opcional)
              └── Planes disponibles
              └── Reglas de cobertura
```

**Estructura futura preparada**:
```
Región (opcional, nivel superior)
  └── Municipio
        └── Zona (opcional, nivel intermedio)
              └── Colonia/Comunidad
                    └── Subzona (opcional, nivel más fino)
                          └── Cobertura
                                └── Planes disponibles
                                └── Reglas de cobertura
```

**Características de la jerarquía**:
- Cada nivel es opcional excepto Municipio y Colonia/Comunidad en V1.
- La jerarquía puede expandirse sin romper relaciones existentes.
- Las solicitudes históricas mantienen referencia a la zona original aunque la jerarquía cambie.
- Los planes asociados a una zona se conservan aunque la zona se mueva dentro de la jerarquía.

### Modelo de Cobertura V1

**Cobertura binaria**:
- En V1, la cobertura es binaria: una zona tiene cobertura o no tiene cobertura.
- Si tiene cobertura, se configuran planes disponibles y costos de instalación.
- Si no tiene cobertura, la zona existe en el catálogo pero no muestra planes.

**Reglas de cobertura V1**:
- **Disponibilidad**: Cobertura activa o inactiva.
- **Planes disponibles**: Lista de planes que se pueden contratar en esa zona.
- **Costo de instalación**: Puede variar por zona o plan.
- **Notas**: Información adicional sobre la cobertura (ej: "requiere factibilidad técnica").

### Análisis de Demanda por Zona

**Análisis básico V1**:
- Conteo de solicitudes por municipio y colonia.
- Agrupación por estado (pendiente, contactado, agendado, cancelado).
- Identificación de zonas con alta concentración de solicitudes.
- Diferenciación entre solicitudes con cobertura y sin cobertura.

**Propósito del análisis V1**:
- Permitir que ventas priorice zonas con mayor demanda.
- Identificar zonas sin cobertura pero con alta demanda (candidatas para expansión).
- Detectar patrones geográficos en solicitudes.
- Apoyar decisiones de expansión de red.

---

## Modelo de Datos Conceptual

### Entidades Principales

**Municipio**
- id
- nombre
- estado
- activo (booleano)
- creado_por (usuario_id)
- fecha_creación (timestamp)
- actualizado_por (usuario_id, nullable)
- fecha_modificación (timestamp)

**Colonia/Comunidad**
- id
- municipio_id (relación con Municipio)
- nombre
- tipo (colonia | comunidad | ranchería | otra)
- activo (booleano)
- creado_por (usuario_id)
- fecha_creación (timestamp)
- actualizado_por (usuario_id, nullable)
- fecha_modificación (timestamp)

**Cobertura**
- id
- colonia_id (relación con Colonia/Comunidad)
- activa (booleano)
- tipo_cobertura (total | parcial | condicional | planificada) - V1 solo usa "total" y "planificada"
- fecha_activación (timestamp)
- fecha_desactivación (timestamp, nullable)
- notas (texto, opcional)
- reglas (json, nullable - para reglas futuras por área)
- creado_por (usuario_id)
- fecha_creación (timestamp)
- actualizado_por (usuario_id, nullable)
- fecha_modificación (timestamp)

**Plan**
- id
- nombre
- velocidad_descarga (Mbps)
- velocidad_subida (Mbps)
- precio_mensual (decimal)
- descripción (texto, opcional)
- activo (booleano)
- orden (integer - para ordenamiento en vista pública)
- destacado (booleano - para marcar plan recomendado)
- creado_por (usuario_id)
- fecha_creación (timestamp)
- actualizado_por (usuario_id, nullable)
- fecha_modificación (timestamp)

**Disponibilidad de Plan por Zona**
- id
- cobertura_id (relación con Cobertura)
- plan_id (relación con Plan)
- costo_instalación (decimal, puede variar por zona)
- disponible (booleano - para activar/desactivar plan específico en zona)
- creado_por (usuario_id)
- fecha_creación (timestamp)

**Solicitud de Instalación**
- id
- nombre_prospecto
- telefono_contacto
- direccion_especifica
- municipio_id (relación con Municipio)
- colonia_id (relación con Colonia/Comunidad)
- plan_id (relación con Plan, nullable si es lead sin cobertura)
- costo_instalacion_cotizado (decimal, nullable)
- precio_mensual_cotizado (decimal, nullable)
- estado (pendiente | contactado | agendado | cancelado | duplicado)
- origen (portal | teléfono | whatsapp | presencial | otro)
- tipo (solicitud_cobertura | lead_sin_cobertura)
- solicitud_duplicada_de (solicitud_id, nullable)
- fecha_solicitud (timestamp)
- fecha_actualizacion (timestamp)
- creado_por (usuario_id, nullable - null si es de portal público)
- actualizado_por (usuario_id, nullable)

**Nota de Solicitud**
- id
- solicitud_id (relación con Solicitud)
- usuario_id (relación con Usuario Administrativo)
- texto (texto)
- fecha_creación (timestamp)

**Usuario Administrativo**
- id
- nombre
- email
- password_hash
- rol (superadministrador | administrador | ventas)
- activo (booleano)
- fecha_creacion (timestamp)
- ultimo_acceso (timestamp, nullable)

### Relaciones Clave

- Un Municipio tiene muchas Colonias/Comunidades.
- Una Colonia/Comunidad puede tener una Cobertura (relación uno a uno opcional).
- Una Cobertura tiene muchos Planes disponibles (relación muchos a muchos a través de Disponibilidad de Plan por Zona).
- Una Solicitud pertenece a un Municipio y una Colonia/Comunidad.
- Una Solicitud puede tener un Plan (nullable si es lead sin cobertura).
- Una Solicitud tiene muchas Notas (relación uno a muchos).
- Una Solicitud puede estar marcada como duplicada de otra Solicitud.
- Un Usuario Administrativo puede crear muchas Solicitudes y Notas.

### Campos de Auditoría

Todas las entidades principales incluyen:
- **creado_por**: ID del usuario que creó el registro.
- **fecha_creación**: Timestamp de creación.
- **actualizado_por**: ID del usuario que modificó el registro (nullable).
- **fecha_modificación**: Timestamp de última modificación.

Estos campos permiten trazabilidad completa y auditoría de cambios.

### Preparación para Expansión Futura

**Campos preparados para evolución**:
- **tipo_cobertura** en Cobertura: Para cobertura parcial, condicional o planificada.
- **reglas** en Cobertura (JSON): Para reglas complejas por área sin cambiar esquema.
- **tipo** en Solicitud: Para diferenciar solicitudes con cobertura de leads sin cobertura.
- **orden y destacado** en Plan: Para control de presentación en vista pública.

**Estructura preparada para nuevos niveles jerárquicos**:
- El modelo actual puede expandirse con entidades Region, Zona, Subzona sin romper relaciones existentes.
- Las solicitudes mantienen referencia a municipio_id y colonia_id, que seguirán existiendo aunque se agreguen niveles intermedios.
- La cobertura puede asociarse a cualquier nivel de la jerarquía en el futuro.

---

## Reglas de Negocio

**RN-001**: La cobertura se determina por catálogo, no por coordenadas geográficas o mapas GIS. Una ubicación tiene cobertura si existe un registro activo en la tabla Cobertura para esa colonia o comunidad.

**RN-002**: Solo se muestran planes disponibles en la zona con cobertura. Si una zona tiene cobertura pero no tiene planes asociados, se muestra mensaje indicando que la cobertura está próxima.

**RN-003**: La cotización estimada incluye el costo de instalación (costo estándar base + ajuste por zona, si aplica) y el precio mensual del plan seleccionado. La cotización debe indicar claramente que es estimada y sujeta a validación técnica. El monto final puede variar después de evaluación técnica.

**RN-004**: Todas las solicitudes se registran inicialmente con estado "pendiente" y origen según el canal (portal, teléfono, etc.).

**RN-005**: Solo usuarios administrativos autenticados pueden acceder al panel de gestión de solicitudes.

**RN-006**: El estado de una solicitud solo puede ser cambiado por un usuario administrativo.

**RN-007**: Las solicitudes canceladas o duplicadas no se eliminan del sistema, solo cambian de estado.

**RN-008**: El número de teléfono debe validarse como 10 dígitos numéricos (formato mexicano).

**RN-009**: La dirección específica es obligatoria para solicitudes con cobertura disponible, pero opcional para solicitudes de "avisar cuando haya cobertura".

**RN-010**: Las notas internas agregadas por el administrador no son visibles para el prospecto.

**RN-011**: Antes de crear una nueva solicitud, el sistema debe verificar si existe otra solicitud con el mismo teléfono en los últimos 7 días con estado "pendiente". Si existe, mostrar mensaje al prospecto y no permitir crear duplicada.

**RN-012**: Un administrador puede marcar una solicitud como duplicada de otra. Las solicitudes duplicadas no cuentan para métricas de conversión.

**RN-013**: Solo superadministradores pueden modificar el catálogo de cobertura, planes, costos y usuarios administrativos.

**RN-014**: Los planes inactivos no aparecen en vista pública pero se conservan en solicitudes históricas para referencia.

**RN-015**: Las sesiones de administrador expiran después de 30 minutos de inactividad.

**RN-016**: Una zona geográfica puede existir sin cobertura. Esto permite mantener catálogo territorial completo aunque no todas las zonas tengan servicio activo.

**RN-017**: Las solicitudes mantienen referencia a la zona geográfica original aunque la jerarquía territorial cambie. Esto preserva integridad de datos históricos.

**RN-018**: El análisis de demanda por zona incluye tanto solicitudes con cobertura como sin cobertura, permitiendo identificar oportunidades de expansión.

**RN-019**: La jerarquía territorial puede expandirse con nuevos niveles (región, zona, subzona) sin romper relaciones existentes ni solicitudes históricas.

**RN-020**: Las reglas de cobertura pueden expandirse en el futuro sin requerir refactor del modelo base. El diseño actual prepara la estructura para reglas más complejas.

**RN-021**: Al desactivar una zona de cobertura con solicitudes pendientes activas, el sistema debe solicitar confirmación explícita del superadministrador.

**RN-022**: Las solicitudes sin cobertura (leads) se registran con tipo "lead_sin_cobertura" y no requieren plan seleccionado. Estas solicitudes alimentan el análisis de demanda para expansión.

**RN-023**: El campo "reglas" en Cobertura puede almacenar configuración adicional en formato JSON para futuras reglas por área sin requerir cambios en el esquema de base de datos.

**RN-024**: El portal es público y accesible desde internet sin restricciones de red.

**RN-025**: La contratación formal del servicio requiere contrato firmado entre el cliente y Internet Regional. El portal solo captura la solicitud, no gestiona la firma del contrato.

---

## Riesgos y Dependencias

### Riesgos

**R-001**: **Datos de cobertura incompletos o inexactos**. Si el catálogo de cobertura no está bien mantenido, los prospectos pueden recibir información incorrecta.
- **Mitigación**: Establecer proceso claro de actualización del catálogo y responsable asignado (superadministrador).

**R-002**: **Prospectos no encuentran su ubicación exacta**. Si la nomenclatura de colonias o comunidades no coincide con lo que el prospecto conoce, puede abandonar el proceso.
- **Mitigación**: Incluir campo de búsqueda con autocompletado y permitir búsqueda parcial. Mostrar mensaje claro si no se encuentra la ubicación.

**R-003**: **Solicitudes sin seguimiento**. Si el equipo de ventas no revisa regularmente las solicitudes, los prospectos pueden perder interés.
- **Mitigación**: Establecer SLA interno de contacto (ej: máximo 24 horas) y vista de solicitudes pendientes antiguas destacada.

**R-004**: **Cotizaciones inexactas**. Si el costo de instalación varía significativamente según la ubicación específica, la cotización estimada puede generar expectativas incorrectas.
- **Mitigación**: Dejar claro en la interfaz que la cotización es estimada y sujeta a validación técnica durante el contacto.

**R-005**: **Adopción del panel administrativo**. Si el equipo de ventas no usa el panel consistentemente, se pierde visibilidad y seguimiento.
- **Mitigación**: Capacitación inicial y establecimiento de procesos claros de uso.

### Dependencias

**D-001**: **Catálogo de cobertura**. El sistema depende de que Internet Regional proporcione el catálogo completo y actualizado de zonas con cobertura.

**D-002**: **Definición de planes y precios**. El sistema requiere que los planes, velocidades y precios estén definidos antes de la implementación.

**D-003**: **Acceso a infraestructura de hosting**. Se requiere un servidor web y base de datos para desplegar el sistema.

**D-004**: **Definición de usuarios administrativos iniciales**. Se requiere identificar quiénes serán los primeros usuarios del panel administrativo y sus roles.

**D-005**: **Activos de marca**. Se requieren logo, colores corporativos y lineamientos de branding de Internet Regional para el diseño visual final.

---

## Exclusiones de Alcance

Lo siguiente está explícitamente fuera del alcance de la primera versión:

**E-001**: Mapas interactivos con GIS, coordenadas geográficas o visualización en mapa de cobertura.

**E-002**: Pagos en línea o integración con pasarelas de pago.

**E-003**: Agendamiento automático de citas de instalación con calendario.

**E-004**: Sistema de cuentas de usuario para prospectos (registro, login, historial de solicitudes).

**E-005**: Integración con sistemas de provisión técnica o activación automática del servicio.

**E-006**: Notificaciones automáticas por correo electrónico o SMS al prospecto.

**E-007**: Reportes avanzados, dashboards analíticos o métricas de conversión complejas.

**E-008**: Sistema de tickets o soporte al cliente.

**E-009**: Validación técnica automática de factibilidad de instalación (distancia a nodo, disponibilidad de puertos, etc.).

**E-010**: Multi-idioma. El sistema será únicamente en español.

**E-011**: Aplicación móvil nativa. El sistema será una aplicación web responsiva.

**E-012**: Integración con redes sociales o WhatsApp Business.

**E-013**: Cobertura granular por subzonas o manzanas (preparado para evolución futura, no implementado en V1).

**E-014**: Asignación automática de solicitudes a vendedores específicos.

**E-015**: Gestión electrónica de firma de contratos.

**E-016**: Generación automática de documentos contractuales.

**E-017**: Almacenamiento de contratos firmados en el sistema.

**E-018**: Flujo de aprobación de contratos dentro del portal.

**E-019**: Integración con sistemas de gestión documental externa.

---

## Criterios de Aceptación

### Vista Pública

**CA-001**: Un prospecto puede ingresar al portal, seleccionar su municipio y colonia, y obtener respuesta sobre disponibilidad de cobertura en menos de 10 segundos.

**CA-002**: Si hay cobertura, el prospecto puede ver al menos un plan disponible con su precio mensual y velocidades en formato de tarjetas visuales.

**CA-003**: El prospecto puede completar el formulario de solicitud con sus datos de contacto y recibir confirmación inmediata con número de solicitud.

**CA-004**: Si no hay cobertura, el prospecto puede dejar sus datos para ser contactado cuando haya cobertura en su zona.

**CA-005**: El formulario valida correctamente los campos obligatorios y muestra mensajes de error claros y específicos.

**CA-006**: La vista pública es completamente funcional en dispositivos móviles (320px a 1440px).

**CA-007**: El sistema detecta y previene solicitudes duplicadas (mismo teléfono en últimos 7 días).

**CA-008**: La cotización mostrada indica claramente que es estimada y sujeta a validación técnica.

**CA-009**: El portal muestra aviso visible de que la contratación formal requiere contrato firmado.

### Vista Administrativa

**CA-010**: Un administrador puede iniciar sesión con sus credenciales y acceder al panel de solicitudes.

**CA-011**: El administrador puede ver todas las solicitudes pendientes con su información completa (nombre, teléfono, ubicación, plan, origen).

**CA-012**: El administrador puede filtrar solicitudes por estado y ver solo las pendientes.

**CA-013**: El administrador puede cambiar el estado de una solicitud de "pendiente" a "contactado", "agendado", "cancelado" o "duplicado".

**CA-014**: El administrador puede agregar múltiples notas internas a una solicitud, cada una con timestamp y usuario.

**CA-015**: El administrador puede ver un resumen de solicitudes agrupadas por municipio o colonia con conteos por estado.

**CA-016**: El administrador puede exportar la lista de solicitudes a CSV o Excel respetando filtros aplicados.

**CA-017**: El administrador puede marcar una solicitud como duplicada de otra.

### Gestión de Cobertura

**CA-018**: Un superadministrador puede agregar nuevas zonas de cobertura al catálogo.

**CA-019**: Un superadministrador puede asociar planes disponibles a una zona de cobertura.

**CA-020**: Un superadministrador puede configurar el costo estándar base de instalación y ajustarlo por zona.

**CA-021**: Un superadministrador puede activar o desactivar cobertura por zona.

**CA-022**: Un superadministrador puede gestionar usuarios administrativos (crear, editar, desactivar).

### General

**CA-023**: El sistema responde en menos de 2 segundos para consultas de cobertura.

**CA-024**: El sistema es responsivo y funciona correctamente en pantallas de 320px a 1440px de ancho.

**CA-025**: Las credenciales de administrador están protegidas con hash seguro y las sesiones expiran después de 30 minutos de inactividad.

**CA-026**: El sistema protege contra ataques comunes (SQL injection, XSS, CSRF).

**CA-027**: Todas las entidades principales registran campos de auditoría (creado_por, fecha_creación, actualizado_por, fecha_modificación).

---

## Evolución Futura

El sistema está diseñado para evolucionar gradualmente. Las siguientes capacidades están preparadas en el modelo de datos pero no se implementan en V1:

**Cobertura y Zonas**:
- Delimitación territorial más fina (subzonas, manzanas, secciones).
- Cobertura parcial o condicional (no solo binaria).
- Reglas más detalladas por área.
- Análisis de demanda más rico: tendencias temporales, comparativas entre zonas.

**Experiencia de Usuario**:
- Prospectos: historial personal de solicitudes, notificaciones automáticas.
- Ventas: análisis detallado, asignación automática por zona, métricas de conversión.
- Superadministradores: herramientas de análisis territorial avanzado.

**Técnica**:
- Migración a framework frontend si el crecimiento lo justifica.
- API REST completa para separar frontend y backend.
- Integraciones con sistemas externos (facturación, provisión, CRM).

---

## Preguntas Abiertas

Las siguientes preguntas deben resolverse antes o durante la implementación:

**P-001**: ¿Se requiere algún tipo de asignación automática de solicitudes a vendedores específicos, o todas las solicitudes son visibles para todo el equipo de ventas?

**P-002**: ¿Se requiere algún tipo de notificación al administrador cuando llega una nueva solicitud, o es suficiente con que revisen el panel periódicamente?

**P-003**: ¿Se requiere algún tipo de validación de que el teléfono sea real (ej: envío de código de verificación por SMS), o es suficiente con validación de formato?

**P-004**: ¿Hay algún requisito legal o regulatorio sobre protección de datos personales que deba considerarse? Ej: aviso de privacidad, consentimiento para tratamiento de datos.

**P-005**: ¿Se requiere algún tipo de backup o retención de datos? ¿Cuánto tiempo se conservan las solicitudes históricas?

---

## Glosario

**Cobertura**: Disponibilidad de infraestructura de red de Internet Regional en una zona geográfica específica que permite ofrecer el servicio de internet. En V1 es binaria (activa/inactiva), preparada para evolucionar a tipos más complejos (parcial, condicional, planificada).

**Zona geográfica**: Entidad que representa una ubicación geográfica dentro de la jerarquía territorial (municipio, colonia, comunidad). Existe independientemente de si hay cobertura o no.

**Jerarquía territorial**: Estructura organizativa de zonas geográficas en niveles. En V1: Municipio → Colonia/Comunidad. Preparada para expandirse con niveles adicionales (Región, Zona, Subzona) en versiones futuras.

**Colonia/Comunidad**: División geográfica administrativa dentro de un municipio. Puede ser colonia (zona urbana), comunidad (zona rural), ranchería u otra denominación local.

**Plan**: Paquete de servicio de internet con velocidades de descarga y subida específicas y un precio mensual determinado.

**Costo estándar base**: Costo de instalación definido por el superadministrador como referencia para todas las zonas. Puede ser ajustado por zona específica según complejidad o condiciones particulares.

**Cotización estimada**: Cálculo aproximado del costo total del servicio incluyendo instalación (costo estándar base + ajuste por zona, si aplica) y mensualidad del plan seleccionado. La cotización está sujeta a validación técnica y el monto final puede variar.

**Contrato firmado**: Documento legal entre el cliente y Internet Regional que formaliza la contratación del servicio. Requisito obligatorio para la instalación del servicio. El portal no gestiona la firma del contrato.

**Solicitud de instalación**: Registro de los datos de un prospecto interesado en contratar el servicio, incluyendo información de contacto, ubicación y plan de interés. Puede ser de tipo "solicitud_cobertura" (con plan) o "lead_sin_cobertura" (sin plan).

**Estado de solicitud**: Etapa del proceso de atención de una solicitud. Valores posibles: pendiente, contactado, agendado, cancelado, duplicado.

**Origen de solicitud**: Canal por el cual se recibió la solicitud. Valores posibles: portal, teléfono, whatsapp, presencial, otro.

**Análisis de demanda por zona**: Proceso de identificar y cuantificar solicitudes por zona geográfica para priorizar acciones comerciales y detectar oportunidades de expansión.

**Superadministrador**: Usuario con permisos completos del sistema, responsable de administrar catálogo de cobertura, zonas geográficas, planes, costos y usuarios.

**Nota interna**: Comentario agregado por un administrador a una solicitud para seguimiento interno. No visible para el prospecto.

**Reglas de cobertura**: Configuración adicional asociada a una zona de cobertura que define disponibilidad, limitaciones o condiciones especiales. En V1 son básicas (texto libre), preparadas para evolucionar a reglas estructuradas (JSON) en versiones futuras.

---

## Historial de Versiones

| Versión | Fecha | Descripción | Autor |
|---------|-------|-------------|-------|
| 1.0 | 2026-07-30 | Versión inicial del documento de especificación | Sistema de Agentes |
| 2.0 | 2026-07-30 | Actualización con branding, stack tecnológico, arquitectura por capas, modelo de cobertura flexible y refinamiento de requisitos | Sistema de Agentes |
| 3.0 | 2026-07-30 | Refinamiento de cobertura y zonas con separación zona geográfica/cobertura, jerarquía territorial, reglas por área, análisis de demanda, experiencia futura por usuario y perspectiva de evolución | Sistema de Agentes |
| 4.0 | 2026-07-30 | Ajuste de enfoque: reducción de protagonismo del mapa, centralización en base operativa (cobertura, zonas, solicitudes, ventas), simplificación de perspectiva futura | Sistema de Agentes |
| 5.0 | 2026-07-30 | Refinamiento final: documento más limpio y ejecutable, compresión de visión futura, eliminación de redundancias, enfoque en operación real | Sistema de Agentes |
| 6.0 | 2026-07-30 | Cierre de decisiones: política de costos (estándar base + ajustes por zona), política de contratación (cotización estimada + contrato firmado), portal público confirmado, eliminación de preguntas resueltas, compresión de evolución futura | Sistema de Agentes |
| 7.0 | 2026-07-30 | Limpieza final: eliminación de duplicados, unificación de reglas, compactación de secciones redundantes | Sistema de Agentes |

---

**Fin del documento**
