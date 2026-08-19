from dotenv import load_dotenv
from utils.garmin_utils import get_weekly_activities
load_dotenv()


def parse_weekly_activities(client):
    """
    Retrieve the user's activities for the last 7 days.
    """

    weekly_activities = get_weekly_activities(client)
    parsed_weekly_runs = parse_weekly_runs(weekly_activities)

    parsed_weekly_activities = {}
    parsed_weekly_activities["weekly_runs"] = parsed_weekly_runs

    return parsed_weekly_activities

def parse_weekly_runs(weekly_runs):
    """
    Parse the user's running activities for the last 7 days.
    """

    parsed_weekly_runs = []
    
    for run in weekly_runs:
        # Extraemos el tipo de run de forma segura
        run_type = run.get("activityType", {}).get("typeKey", "")
        
        # Filtramos: Si es 'running' o 'treadmill_running' (cinta), lo procesamos
        if "running" in run_type:
            
            # ¡Aquí va la "Dieta de la IA"!
            # Pegamos el diccionario limpio que armamos en el paso anterior
            parsed_run = {
                "name": run.get("activityName", "Carrera"),
                "date": run.get("startTimeLocal", "Desconocida"),
                
                # Volumen
                "distance_meters": run.get("distance", 0),
                "duration_seconds": run.get("duration", 0),
                
                # Intensidad
                "average_heart_rate": run.get("averageHR", 0),
                "training_load": run.get("activityTrainingLoad", 0),
                
                # Dinámicas (Usamos get por si una cinta no mide zancada)
                "cadence": run.get("averageRunningCadenceInStepsPerMinute", 0),
                "stride_length_cm": run.get("avgStrideLength", 0),
                "vertical_oscillation_cm": run.get("avgVerticalOscillation", 0),
                "vertical_ratio": run.get("avgVerticalRatio", 0),
                
                # Zonas Cardíacas
                "zone_1": run.get("hrTimeInZone_1", 0),
                "zone_2": run.get("hrTimeInZone_2", 0),
                "zone_3": run.get("hrTimeInZone_3", 0),
                "zone_4": run.get("hrTimeInZone_4", 0),
                "zone_5": run.get("hrTimeInZone_5", 0)
            }
            
            parsed_weekly_runs.append(parsed_run)
    
    return parsed_weekly_runs

