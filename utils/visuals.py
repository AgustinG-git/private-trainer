from datetime import date, datetime
import matplotlib.pyplot as plt
from garmin_utils import get_heart_rate_data

def plot_today_heart_rates():
    """Return a graph with today's heart-rate readings."""

    today = date.today().isoformat()
    readings = get_heart_rate_data()

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

