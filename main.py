from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from agents.ollama_agents import chat_Ollama
from utils.data_merger import parse_weekly_activities
from utils.garmin_utils import garmin_client, get_heart_rate_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Login una vez al arrancar; si falla, el servidor no arranca
    app.state.garmin = garmin_client()
    yield

app = FastAPI(title="AI Coach API", lifespan=lifespan)

# Permitir que el frontend (Next.js) llame a este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Errores de Garmin -> códigos HTTP ---

@app.exception_handler(GarminConnectTooManyRequestsError)
async def garmin_rate_limited(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"detail": "Garmin limita las peticiones. Prueba más tarde."},
    )

@app.exception_handler(GarminConnectAuthenticationError)
@app.exception_handler(GarminConnectConnectionError)
async def garmin_unavailable(request: Request, exc: Exception):
    return JSONResponse(
        status_code=502,
        content={"detail": f"Error al consultar Garmin: {exc}"},
    )

# --- Endpoints (def, no async: el código es bloqueante) ---

@app.get("/api/entrenamiento/semanal")
def obtener_plan_semanal(request: Request):
    client = request.app.state.garmin
    weekly_activities = parse_weekly_activities(client, date.today())
    recomendacion = chat_Ollama(weekly_activities, modelo="llama3.2")

    return {
        "actividades": weekly_activities,
        "recomendacion_ia": recomendacion,
    }

@app.get("/api/metricas/frecuencia-cardiaca")
def obtener_pulso_hoy(request: Request):
    client = request.app.state.garmin
    return get_heart_rate_data(client, date.today())
