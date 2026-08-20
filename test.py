from dotenv import load_dotenv
from utils.garmin_utils import garmin_client
from utils.data_merger import parse_weekly_activities
from agents.ollama_agents import chat_Ollama
load_dotenv()

client = garmin_client()

weekly_activities = parse_weekly_activities(client)

print(chat_Ollama(f"""
Actúa como un entrenador de atletismo y fisiólogo deportivo de alto rendimiento.

A continuación, te proporciono los datos de mis actividades de running realizadas esta semana:

[DATOS DE ACTIVIDADES DE LA SEMANA]
{weekly_activities}

Con base en esta información, realiza lo siguiente:

1. Diagnóstico breve:
Analiza el estímulo recibido, la distribución de intensidades y la fatiga acumulada durante la semana.

2. Propuesta de la siguiente semana / ciclo de entrenamiento:
Diseña una rutina semanal estructurada día por día (especificando tipo de sesión, distancia/tiempo objetivo, zonas de frecuencia cardíaca o ritmos recomendados y días de descanso/recuperación activa).

3. Proyección optimista de rendimiento:
Detalla qué mejoras o resultados podría esperar de forma optimista si cumplo esta progresión de manera consistente (por ejemplo: adaptación de ritmos a umbral, eficiencia cardiovascular, evolución esperada de marcas en distancias clave como 5K/10K/Media Maratón y progresión del VO2 máx).

Sé específico con ritmos, zonas de pulso y volúmenes en lugar de dar pautas genéricas.""", modelo="llama3.2"))
