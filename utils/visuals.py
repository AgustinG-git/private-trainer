from datetime import date, datetime
import matplotlib.pyplot as plt
from utils.garmin_utils import get_heart_rate_data

def plot_heart_rates(client, day: date):
    """Return a graph with the heart-rate readings of `day`."""

    readings = get_heart_rate_data(client, day)

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
        axis.text(0.5, 0.5, f"No hay datos de frecuencia cardiaca para {day}",
                  ha="center", va="center", transform=axis.transAxes)

    axis.set_title(f"Frecuencia cardiaca del {day}")
    axis.set_xlabel("Hora")
    axis.set_ylabel("Pulsaciones por minuto (bpm)")
    axis.grid(True, alpha=0.3)
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure

