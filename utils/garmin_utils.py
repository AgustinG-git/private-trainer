from garminconnect import Garmin
import os
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

def garmin_client():
    """
    Create and return a Garmin client using the provided credentials.
    """

    garmin_password = os.getenv("GARMIN_PASSWORD")
    garmin_username = os.getenv("GARMIN_EMAIL")

    client = Garmin(garmin_username, garmin_password)
    try:
        client.login("~/.garminconnect")
        print("Connection successful.")
        return client
    
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def get_weekly_activities(client: Garmin):
    """
    Retrieve the user's activities for the last 7 days.
    """

    today = date.today().isoformat()
    start = (date.today() - timedelta(days=7)).isoformat()  # 7 days ago

    weekly_activities = client.get_activities_by_date(start, today)
    
    return weekly_activities

def get_heart_rate_data(client: Garmin):
    """
    Retrieve the user's heart rate data for the last 7 days.
    """ 
        
    today = date.today().isoformat()
    heart_rate_data = client.get_heart_rates(today)
    readings = heart_rate_data.get("heartRateValues", [])
    
    return readings

def get_sleep_data(client: Garmin):
    """
    Retrieve the user's sleep data for the last 7 days.
    """

    today = date.today().isoformat()
    sleep_data = client.get_sleep_data(today)
    
    return sleep_data

def get_body_battery_data(client: Garmin):
    """
    Retrieve the user's body battery data for the last 7 days.
    """

    today = date.today().isoformat()
    body_battery_data = client.get_body_battery(today)
    
    return body_battery_data

def get_stress_data(client: Garmin):
    """
    Retrieve the user's stress data for the last 7 days.
    """

    today = date.today().isoformat()
    stress_data = client.get_stress(today)
    
    return stress_data

def get_daily_steps(client: Garmin):
    """
    Retrieve the user's daily steps data for the last 7 days.
    """

    today = date.today().isoformat()
    daily_steps_data = client.get_daily_steps(today)
    
    return daily_steps_data

def get_daily_floors(client: Garmin):
    """
    Retrieve the user's daily floors data for the last 7 days.
    """

    today = date.today().isoformat()
    daily_activity_data = client.get_floors(today)
    
    return daily_activity_data

def get_weekly_sleep_data(client):
    """
    Retrieve the user's sleep data for the last 7 days.
    """
    weekly_sleep = []
    
    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            sleep_data = get_sleep_data(client)
            weekly_sleep.append(sleep_data)
        except Exception as e:
            print(f"No se pudo obtener el sueño del {target_date}: {e}")
            
    return weekly_sleep

def get_weekly_heart_rate_data(client: Garmin):
    """
    Retrieve the user's heart rate data for the last 7 days.
    """
    weekly_heart_rate_data = []

    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            heart_rate_data = get_heart_rate_data(client)
            weekly_heart_rate_data.append(heart_rate_data)
        except Exception as e:
            print(f"No se pudo obtener la frecuencia cardíaca del {target_date}: {e}")

    return weekly_heart_rate_data

def get_weekly_body_battery_data(client: Garmin):
    """
    Retrieve the user's body battery data for the last 7 days.
    """
    weekly_body_battery_data = []

    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            body_battery_data = get_body_battery_data(client)
            weekly_body_battery_data.append(body_battery_data)
        except Exception as e:
            print(f"No se pudo obtener la batería corporal del {target_date}: {e}")

    return weekly_body_battery_data

def get_weekly_stress_data(client: Garmin):
    """
    Retrieve the user's stress data for the last 7 days.
    """
    weekly_stress_data = []

    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            stress_data = get_stress_data(client)
            weekly_stress_data.append(stress_data)
        except Exception as e:
            print(f"No se pudo obtener el estrés del {target_date}: {e}")

    return weekly_stress_data

def get_weekly_daily_steps(client: Garmin):
    """
    Retrieve the user's daily steps data for the last 7 days.
    """
    weekly_daily_steps_data = []

    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            daily_steps_data = get_daily_steps(client)
            weekly_daily_steps_data.append(daily_steps_data)
        except Exception as e:
            print(f"No se pudo obtener los pasos diarios del {target_date}: {e}")

    return weekly_daily_steps_data

def get_weekly_daily_floors(client: Garmin):
    """
    Retrieve the user's daily floors data for the last 7 days.
    """
    weekly_daily_floors_data = []

    for i in range(7):
        target_date = (date.today() - timedelta(days=i)).isoformat()
        
        try:
            daily_floors_data = get_daily_floors(client)
            weekly_daily_floors_data.append(daily_floors_data)
        except Exception as e:
            print(f"No se pudo obtener los pisos diarios del {target_date}: {e}")

    return weekly_daily_floors_data
