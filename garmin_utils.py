from garminconnect import Garmin
import os
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt

load_dotenv()

def connection_test():
    """
    Test the connection to Garmin Connect using the provided credentials.
    """

    garmin_password = os.getenv("GARMIN_PASSWORD")
    garmin_username = os.getenv("GARMIN_EMAIL")

    client = Garmin(garmin_username, garmin_password)
    
    try:
        client.login("~/.garminconnect")
        print("Connection successful.")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def get_monthly_activities():
    """
    Retrieve the user's activities for the current month.
    """

    garmin_password = os.getenv("GARMIN_PASSWORD")
    garmin_username = os.getenv("GARMIN_EMAIL")

    client = Garmin(garmin_username, garmin_password)
    client.login("~/.garminconnect")

    today = date.today().isoformat()
    start = date.today().replace(day=1).isoformat()  # Start of the month

    monthly_activities = client.get_activities_by_date(start, today)
    
    return monthly_activities

def get_weekly_activities():
    """
    Retrieve the user's activities for the last 7 days.
    """

    garmin_password = os.getenv("GARMIN_PASSWORD")
    garmin_username = os.getenv("GARMIN_EMAIL")

    client = Garmin(garmin_username, garmin_password)
    client.login("~/.garminconnect")

    today = date.today().isoformat()
    start = (date.today() - timedelta(days=7)).isoformat()  # 7 days ago

    weekly_activities = client.get_activities_by_date(start, today)
    
    return weekly_activities

def plot_today_heart_rates(garmin_client):
    """Return a graph with today's heart-rate readings."""
    
    today = date.today().isoformat()
    heart_rate_data = garmin_client.get_heart_rates(today)
    readings = heart_rate_data.get("heartRateValues", [])

    timestamps = []
    heart_rates = []
    for timestamp, heart_rate in readings:
        if timestamp is None or heart_rate is None:
            continue
        if timestamp > 10**12:
            timestamp /= 1000
        timestamps.append(datetime.fromtimestamp(timestamp))
        heart_rates.append(heart_rate)

    figure, axis = plt.subplots(figsize=(12, 5))
    if heart_rates:
        axis.plot(timestamps, heart_rates, color="#d1495b", linewidth=1.5)
        axis.set_ylim(bottom=max(0, min(heart_rates) - 10))
    else:
        axis.text(0.5, 0.5, "No hay datos de frecuencia cardiaca para hoy",
                  ha="center", va="center", transform=axis.transAxes)

    axis.set_title(f"Frecuencia cardiaca de hoy ({today})")
    axis.set_xlabel("Hora")
    axis.set_ylabel("Pulsaciones por minuto (bpm)")
    axis.grid(True, alpha=0.3)
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure


