from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Importas tus funciones existentes
from utils.garmin_utils import garmin_client, get_heart_rate_data
from utils.data_merger import parse_weekly_activities
from agents.ollama_agents import chat_Ollama

app = FastAPI(title="AI Coach API")

# Permitir que el frontend (React) se comunique con este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Tu futuro frontend en Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/entrenamiento/semanal")
async def obtener_plan_semanal():
    try:
        # 1. Autenticación (por ahora usa tu .env como ya tienes programado)
        client = garmin_client()
        
        # 2. Extraer datos
        weekly_activities = parse_weekly_activities(client)
        
        # 3. Generar recomendación con Llama 3.2
        recomendacion = chat_Ollama(weekly_activities, modelo="llama3.2")
        
        return {
            "actividades": weekly_activities,
            "recomendacion_ia": recomendacion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metricas/frecuencia-cardiaca")
async def obtener_pulso_hoy():
    client = garmin_client()
    hr_data = get_heart_rate_data(client)
    # Devuelves el JSON puro, sin pasar por matplotlib
    return hr_data