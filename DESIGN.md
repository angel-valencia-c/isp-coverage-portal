# Design System — Portal Enlaces Costa Grande

## 1. Objetivo visual

Portal profesional, limpio y orientado a conversión. Debe transmitir confianza, claridad y orden para tres audiencias: prospectos, equipo de ventas y superadministrador.

### Principios
- Claridad sobre decoración.
- Consistencia sistemática.
- Reutilización máxima.
- Mobile-first.
- Accesibilidad básica.
- Evitar improvisación visual entre fases.

---

## 2. Anchor visual: Swiss

Se elige **Swiss** porque transmite precisión, jerarquía y confianza sin ser agresivo. Es el mejor ajuste para un portal comercial de telecomunicaciones que necesita verse serio, claro y fácil de usar.

### Rasgos del anchor
- Superficies blancas o grises neutros.
- Tipografía sans-serif.
- Un color de acento usado con intención.
- Hairline rules para estructura.
- Numeración grande para datos técnicos, precios y conteos.

### No usar
- Fondos cálidos.
- Serif.
- Texturas.
- Sombras decorativas.
- Bordes redondeados grandes.
- Gradientes complejos.

---

## 3. Tokens de diseño

### 3.1 Colores

```css
--color-surface: #FFFFFF;
--color-surface-alt: #F7F7F8;
--color-surface-muted: #EDEFF2;

--color-text: #0A0A0A;
--color-text-secondary: #4A4A4A;
--color-text-muted: #6B6B6B;
--color-text-inverse: #FFFFFF;

--color-accent: #0066FF;
--color-accent-hover: #0052CC;
--color-accent-light: #E6F0FF;

--color-success: #059669;
--color-success-light: #D1FAE5;
--color-error: #DC2626;
--color-error-light: #FEE2E2;
--color-warning: #D97706;
--color-warning-light: #FEF3C7;

--color-border: #D1D5DB;
--color-border-strong: #9CA3AF;
```

### 3.2 Tipografía

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

--text-xs: 0.75rem;
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-xl: 1.25rem;
--text-2xl: 1.5rem;
--text-3xl: 1.875rem;
--text-4xl: 2.5rem;

--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 3.3 Espaciado

```css
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-6: 1.5rem;
--space-8: 2rem;
--space-12: 3rem;
```

### 3.4 Bordes y radios

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-full: 9999px;

--border: 1px solid var(--color-border);
```

---

## 4. Estructura de carpetas

La idea es que estas carpetas sirvan como base reutilizable para que el LLM y el equipo sepan dónde poner cada cosa.

```txt
public/
├── css/
│   ├── tokens.css
│   ├── base.css
│   ├── components.css
│   └── layouts.css
├── js/
│   └── main.js
├── images/
└── fonts/

app/templates/
├── base.html
├── layouts/
│   ├── public.html
│   └── admin.html
├── components/
│   ├── button.html
│   ├── form-field.html
│   ├── card.html
│   ├── table.html
│   ├── badge.html
│   └── alert.html
└── pages/
    ├── public/
    │   ├── index.html
    │   ├── plans.html
    │   └── request.html
    └── admin/
        ├── dashboard.html
        └── requests.html
```

### Propósito
- `tokens.css`: variables globales.
- `base.css`: reset, tipografía y estilo global.
- `components.css`: componentes reutilizables.
- `layouts.css`: reglas de layout por contexto.
- `base.html`: estructura HTML general.
- `layouts/`: layouts por tipo de vista.
- `components/`: piezas reutilizables.
- `pages/`: templates concretos por pantalla.

---

## 5. Reglas de implementación

### 5.1 Templates

- Toda página debe heredar de un layout.
- Los componentes se reutilizan con `{% include %}`.
- No se duplica HTML si ya existe un componente.
- Los bloques base deben ser `title`, `content` y `scripts`.

Ejemplo:

```jinja2
{% extends "layouts/public.html" %}

{% block content %}
  <h1>Verifica tu cobertura</h1>
{% endblock %}
```

### 5.2 CSS

- Usar siempre variables.
- Evitar valores hardcodeados.
- Aplicar enfoque mobile-first.
- Definir una sola vez botones, formularios, tablas, cards y badges.
- No usar `!important`.

Ejemplo:

```css
.btn {
  background: var(--color-accent);
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
}
```

### 5.3 Componentes base

#### Button
- Variantes: `primary`, `secondary`, `full`.
- Debe ser consistente en todo el sistema.

#### Form field
- Label arriba.
- Input con focus visible.
- Error debajo.
- Validación clara.

#### Card
- Usada para planes, métricas, bloques informativos y resúmenes.

#### Table
- Usada para administración y listados.
- Debe ser legible, limpia y con hover sutil.

#### Badge
- Usada para estados como éxito, advertencia y error.

---

## 6. Reglas de layout

### Vista pública
- Contenedor centrado.
- Max-width de 1280px.
- Espaciado generoso.
- Header simple.
- Footer funcional.

### Panel administrativo
- Sidebar fijo en desktop.
- Drawer en mobile.
- Tablas ocupan todo el ancho.
- Densidad media-alta.
- Priorizar eficiencia operativa.

---

## 7. Reglas de consistencia

- Los mismos componentes deben verse igual en todos los módulos.
- Los mismos estados deben usar los mismos colores.
- Los formularios deben validar igual en todo el sistema.
- Los mensajes de error deben ser claros y específicos.
- No se debe inventar contenido falso.
- No se debe cambiar el copy estándar de UI sin necesidad.

### Estados estándar
- `hover`
- `focus`
- `disabled`
- `loading`
- `error`

---

## 8. Qué no hacer

- No mezclar estilos entre módulos.
- No hardcodear colores o medidas.
- No duplicar componentes.
- No usar sombras decorativas.
- No usar fondos cálidos.
- No usar serif.
- No usar copy temático innecesario.
- No inventar datos para “llenar” la UI.
- No romper el sistema visual por pantalla nueva.

---

## 9. Relación con fases futuras

### Fase 3
Gestión de cobertura, CRUDs y administración territorial.

### Fase 4-6
Portal público: buscador, planes y solicitud.

### Fase 7-9
Panel administrativo: dashboard, filtros, detalles y métricas.

### Fase 10
Endurecimiento: consistencia visual, accesibilidad y performance.

---

## 10. Archivos base a crear

Orden sugerido para implementación:

1. `public/css/tokens.css`
2. `public/css/base.css`
3. `public/css/components.css`
4. `public/css/layouts.css`
5. `app/templates/base.html`
6. `app/templates/layouts/public.html`
7. `app/templates/layouts/admin.html`
8. `app/templates/components/`

---

## 11. Checklist rápido

- [ ] ¿Usé variables CSS?
- [ ] ¿Reutilicé componentes?
- [ ] ¿Es mobile-first?
- [ ] ¿Los estados están definidos?
- [ ] ¿Se ve limpio y profesional?
- [ ] ¿No inventé datos?
- [ ] ¿No rompí la consistencia?

---

**Fin del documento**