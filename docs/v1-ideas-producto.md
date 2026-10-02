# private-trainer v1: ideas de producto y diseño

Fecha: 2 oct 2026 · Estado: propuesta · Complementa a `plan-v1.md`

> **Cambio respecto a `plan-v1.md`:** allí el frontend quedaba fuera de la v1 (la v1 era un informe Markdown por CLI). Este documento redefine la v1 como un **prototipo visual pulido** sobre el mismo backend. Las fases 0-4 del plan siguen siendo necesarias: el front consume el `WeeklySummary`, no JSON crudo de Garmin.

## 1. Concepto

**"El coach que lee tu semana."**

No es otro dashboard de Garmin. Garmin Connect ya muestra datos; lo que aporta esta app es **interpretación híbrida**: carrera, gimnasio y recuperación juntos. Garmin no puede hacerlo porque no conoce tu gimnasio.

**Momento estrella:** el lunes por la mañana abres la app y te espera una "carta" con tu semana, escrita por el coach y respaldada por cifras que puedes comprobar.

**Principio de diseño:** la app tiene opinión. Cada pantalla responde a una pregunta concreta antes de enseñar datos.

| Pantalla | Pregunta que responde |
|---|---|
| Hoy | ¿Qué puedo hacer hoy? |
| Semana | ¿Cómo me ha ido y por qué? |
| Plan | ¿Qué hago la semana que viene? |

## 2. Ideas, ordenadas por impacto

### 2.1 La carta del lunes (pantalla Semana)

Formato editorial, no de dashboard:

- **Titular generado**, por ejemplo: *"Semana de carga: +18 % de volumen, HRV estable, piernas al límite."*
- **3-4 KPIs grandes** con delta frente a la media de 4 semanas (volumen de carrera, tonelaje, % en Z1-2, HRV).
- **Nota del coach** mostrada en streaming, como si se estuviera escribiendo.

### 2.2 Cifras verificables (la idea diferencial)

Cada número que el coach menciona en el texto se muestra como un **chip**. Al pasar el ratón o tocarlo, se resalta el dato de origen en la gráfica correspondiente.

- Es la cara visible del principio *"el LLM no inventa números"* del plan.
- Implementación: el LLM devuelve texto con referencias (`{{metric:run_volume_km}}`) y el front las sustituye por chips con el valor del `WeeklySummary`. Si el LLM cita una métrica que no existe, se detecta antes de mostrar nada.
- Genera confianza y casi ninguna app de IA lo hace.

### 2.3 Mapa muscular

Silueta frontal y dorsal con los grupos musculares coloreados según las series de la semana (datos de FitNotes).

- Escala secuencial de un solo color: 0 series → gris, objetivo alcanzado → acento lleno.
- Demuestra de un vistazo que la app entiende el gimnasio, no solo la carrera.

### 2.4 Calendario híbrido de la semana

Franja de 7 días con bloques de carrera y de fuerza, cada uno con su color.

- **Planificado:** contorno discontinuo. **Realizado:** relleno. La adherencia se ve sin leer.
- **Marca de interferencia:** aviso cuando hay calidad de carrera (series, tempo) en las 24-48 h después de un día de piernas.

### 2.5 Semáforo de hoy (pantalla Hoy)

Anillo con HRV, sueño y Body Battery frente a la línea base de 28 días, más una sola frase:

> *"Verde: hoy puedes hacer calidad."*

Es la pantalla que abrirías cada mañana. Tres estados: verde (calidad), ámbar (suave o técnica), rojo (descanso o movilidad).

### 2.6 Polarización 80/20

Barra apilada con el tiempo en Z1-2 frente a Z3-5 de la semana, con una marca del objetivo (80 %). Simple, legible y muy "de corredor que sabe".

### 2.7 Plan de la próxima semana en tarjetas (pantalla Plan)

Una tarjeta por día: tipo de sesión, duración o distancia, zona o ritmo objetivo y foco.

- Botón **"pedir alternativa"** en cada tarjeta: el coach regenera solo esa sesión respetando el resto de la semana y las restricciones del perfil.
- El plan aceptado se guarda y alimenta el "planificado" del calendario de la semana siguiente.

### 2.8 Tendencia de e1RM

Sparklines de los 4-5 ejercicios clave (press banca, dominadas lastradas, sentadilla…), con una insignia cuando hay PR.

### 2.9 Glifos de ruta (v1.1)

Cada carrera con su recorrido GPS dibujado como una línea SVG fina, sin mapa debajo. Bonito y barato: Garmin devuelve la polilínea en el detalle de la actividad.

### 2.10 El año en una cuadrícula (v1.1)

Heatmap estilo contribuciones de GitHub: 365 días coloreados por tipo de actividad e intensidad por carga. Es la cara visible del contexto histórico del agente.

## 3. Identidad visual

### Tono

Oscuro por defecto, deportivo y sobrio. Los datos son los protagonistas; la decoración, mínima.

### Color

Un color fijo por dominio en toda la app (gráficas, chips, calendario, iconos):

| Dominio | Uso | Propuesta |
|---|---|---|
| Carrera | Bloques, volumen, zonas | Naranja / coral |
| Fuerza | Bloques, mapa muscular, e1RM | Violeta / índigo |
| Recuperación | HRV, sueño, Body Battery | Verde azulado |
| Estado | Semáforo | Verde / ámbar / rojo, solo en Hoy |

Validar el contraste en claro y en oscuro antes de fijar los valores.

### Tipografía

- **Cifras:** fuente condensada (Barlow Condensed u Oswald) con dígitos tabulares (`font-variant-numeric: tabular-nums`).
- **Texto:** Inter o similar.
- La nota del coach, a un tamaño cómodo de lectura y con un ancho máximo de ~65 caracteres.

### Movimiento

Sutil y con propósito:

- Las cifras de los KPIs se cuentan hacia arriba al cargar.
- La nota del coach llega en streaming.
- Las tarjetas aparecen escalonadas.
- Respetar `prefers-reduced-motion`.

### Stack

Sobre lo que ya hay (Next 16 + Tailwind 4):

- **shadcn/ui** para componentes base.
- **Recharts** para gráficas.
- **Framer Motion** para animaciones.
- **lucide-react** para iconos.

## 4. Para que el prototipo no sea humo

- **Modo demo con datos reales congelados:** un snapshot JSON de 2-3 semanas reales en `fixtures/`, generado por el pipeline. La app luce igual sin conectarse a Garmin, que puede bloquear el login (429 / Cloudflare) en el peor momento.
- **Contrato primero:** definir el esquema de `WeeklySummary` (pydantic → JSON Schema → tipos TypeScript) antes de construir pantallas. Con el contrato fijado, front y backend avanzan en paralelo.
- **Riesgo a evitar:** datos inventados a mano que lucen bien pero esconden que la parte difícil no funciona. Las fixtures deben salir del pipeline real, nunca escribirse a mano.

### Esbozo del contrato

```python
class WeeklySummary(BaseModel):
    week: str                    # "2026-W40"
    headline: str                # titular del coach
    kpis: list[Kpi]              # valor, unidad, delta vs 4 sem
    run: RunMetrics              # km, ritmo, zonas, tirada larga
    gym: GymMetrics              # series/grupo, tonelaje, e1RM
    recovery: RecoveryMetrics    # HRV, FC reposo, sueño, BB
    calendar: list[DayBlock]     # planificado vs realizado
    interference: list[Alert]    # conflictos piernas/calidad
    coach_note: str              # texto con {{metric:...}}
    next_week_plan: list[PlannedSession]
```

## 5. Alcance de la v1

| Entra en la v1 | v1.1 | Fuera (v2) |
|---|---|---|
| Pantalla **Hoy** (semáforo) | Glifos de ruta | Chat libre multi-turno |
| Pantalla **Semana** (carta, KPIs, calendario, mapa muscular, 80/20, e1RM) | Heatmap anual | Agente con herramientas SQL |
| Pantalla **Plan** (tarjetas + pedir alternativa) | | Auth y multiusuario |
| Chips de cifras verificables | | Despliegue en la nube |
| Modo demo con fixtures | | Sync automático de FitNotes |

Tres pantallas muy pulidas en lugar de siete a medias.

## 6. Criterios de aceptación

1. Las tres pantallas funcionan en modo demo con fixtures reales y en modo live con el backend.
2. Ninguna cifra mostrada se escribe a mano: todas vienen del `WeeklySummary`.
3. Cada número citado por el coach es un chip enlazado a su dato de origen; las referencias inválidas se detectan y no se muestran.
4. Se ve bien en escritorio y en móvil (≥ 375 px), en modo oscuro y claro.
5. "Pedir alternativa" regenera una sola sesión sin romper las restricciones del perfil.
6. Usada con datos reales al menos dos lunes, y ha cambiado al menos una decisión de entrenamiento.

## 7. Orden de construcción sugerido

1. Fases 0-3 de `plan-v1.md` (higiene, datos, FitNotes, métricas) → `WeeklySummary` con tests.
2. Exportar el contrato a TypeScript y generar las primeras fixtures.
3. Esqueleto del front: layout, navegación, tema, tokens de color y tipografía.
4. Pantalla **Semana** (es la estrella; si solo da tiempo a una, esta).
5. Fase 4 del plan (coach LLM) con salida estructurada y referencias `{{metric:...}}` → chips.
6. Pantallas **Hoy** y **Plan**.
7. Pulido: animaciones, estados vacíos y de carga, responsive.
