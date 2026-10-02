# private-trainer

Coach de entrenamiento híbrido (carrera + gimnasio) que cruza tus datos de Garmin Connect y FitNotes y cada lunes te escribe una carta con tu semana.

> **Estado:** en desarrollo hacia la v1. Fecha objetivo: 9 nov 2026.

## Objetivo de la v1: la carta del lunes

Cada lunes se genera un informe HTML de la semana anterior con carrera, gimnasio y recuperación, comparado con tu media de 4 semanas, y con un plan para la semana siguiente que respeta tus restricciones. **Cada cifra que cita el coach es verificable.**

Criterios de aceptación:

1. `uv run python -m coach report` genera `reports/AAAA-Www.html` (y `.md`) en menos de 2 minutos. El único paso manual es exportar el CSV de FitNotes.
2. La carta incluye: titular, KPIs con variación frente a 4 semanas, carrera (km, ritmo, 80/20, tirada larga), gimnasio (series por grupo, tonelaje, e1RM, PRs), recuperación (HRV, FC en reposo, sueño, Body Battery con semáforo), planificado frente a realizado y alertas de interferencia piernas/calidad.
3. Todas las cifras salen de código determinista con tests. El LLM solo puede citarlas mediante referencias `{{metric:id}}`, que se validan.
4. El plan respeta el perfil del atleta y se guarda como "planificado" de la semana siguiente.
5. Se ha usado dos lunes reales y ha cambiado al menos una decisión de entrenamiento.

**Fuera de la v1:** frontend (v1.1, rama `frontend`), multiusuario, chat, despliegue en la nube.

## Puesta en marcha

Requisitos: [uv](https://docs.astral.sh/uv/), [Ollama](https://ollama.com/download) y una cuenta de Garmin Connect.

```powershell
uv sync                      # crea .venv e instala el lock
Copy-Item .env.example .env  # y rellena tus credenciales
ollama pull llama3.2
uv run test.py
```

`uv` instala por sí solo la versión de Python fijada en `.python-version`.

## Estructura

```text
agents/    # llamada al LLM (Ollama)
utils/     # cliente Garmin, limpieza de datos, gráficos
main.py    # API FastAPI (wip)
test.py    # flujo de prueba de extremo a extremo
docs/      # ideas de producto
```

## Ramas

- `main`: la v1 (Python).
- `frontend`: app Next.js, aparcada hasta la v1.1.
