import os
from datetime import date, datetime

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from garminconnect import Garmin
from utils.garmin_utils import connection_test, get_monthly_activities, get_weekly_activities, plot_today_heart_rates
from utils.data_merger import get_weekly_activities

load_dotenv()

client = Garmin(os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD"))
client.login("~/.garminconnect")

# monthly_activities = get_monthly_activities()
# weekly_activities = get_weekly_activities()

# heart_rate_figure = plot_today_heart_rates(client)
# plt.show()

weekly_activities = get_weekly_activities(client)
#### Distintos Prints ####

print("\n=== Actividades de los ultimos 7 dias ===")

print(f"Total de actividades: {len(weekly_activities)}")
print(weekly_activities)

# print("\n=== Actividades del mes actual ===")
# print(f"Periodo: {first_day} -> {today}")
# print(f"Total de actividades: {len(monthly_activities)}")
# print(monthly_activities)


# print(f"Sleep: {sleep_data.get('totalSleepSeconds', 'n/a')} seconds")