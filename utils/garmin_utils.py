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



def get_weekly_activities(client):
    """
    Retrieve the user's activities for the last 7 days.
    """

    today = date.today().isoformat()
    start = (date.today() - timedelta(days=7)).isoformat()  # 7 days ago

    weekly_activities = client.get_activities_by_date(start, today)
    
    return weekly_activities

def get_heart_rate_data(client):
    """
    Retrieve the user's heart rate data for the last 7 days.
    """ 
        
    today = date.today().isoformat()
    heart_rate_data = client.get_heart_rates(today)
    readings = heart_rate_data.get("heartRateValues", [])
    
    return readings
