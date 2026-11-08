from collections.abc import Callable
from datetime import date, timedelta
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

load_dotenv()

TOKENSTORE = Path("~/.garminconnect").expanduser()
TOKEN_FILE = TOKENSTORE / "garmin_tokens.json"
INVALID_TOKEN_FILE = TOKENSTORE / "garmin_tokens.invalid.json"

class GarminLoginError(Exception):
    """Login to Garmin failed; the message says why."""

class GarminRateLimitError(GarminLoginError):
    """Garmin is rate limiting this IP (429). Temporary."""

def garmin_client() -> Garmin:
    """
    Return a logged-in Garmin client.

    Translates the library errors into GarminLoginError so
    callers only need to handle one exception type.
    """

    try:
        return _connect()
    except GarminConnectTooManyRequestsError as e:
        raise GarminRateLimitError(
            "Garmin está limitando tu IP (429). Espera unos minutos."
        ) from e
    except GarminConnectAuthenticationError as e:
        raise GarminLoginError(f"Garmin rechazó las credenciales: {e}") from e
    except GarminConnectConnectionError as e:
        raise GarminLoginError(f"No se pudo conectar con Garmin: {e}") from e

def _connect() -> Garmin:
    """
    Log in with saved tokens; fall back to email/password once.
    """

    if TOKEN_FILE.exists():
        try:
            client = Garmin()  # sin credenciales: solo tokens
            client.login(str(TOKENSTORE))
            return client
        except GarminConnectAuthenticationError:
            print("Tokens de Garmin caducados: login con contraseña.")
            TOKEN_FILE.replace(INVALID_TOKEN_FILE)  # apartar, no borrar

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    if not email or not password:
        raise GarminLoginError(
            "Define GARMIN_EMAIL y GARMIN_PASSWORD en el .env"
        )

    client = Garmin(email, password)
    client.login(str(TOKENSTORE))  # sin tokens: login y los guarda
    return client

def get_weekly_activities(client: Garmin, end: date) -> list[dict]:
    """
    Retrieve the activities of the 7 days ending on `end` (inclusive).
    """

    start = end - timedelta(days=6)  # 7 días contando `end`
    return client.get_activities_by_date(start.isoformat(), end.isoformat())

# --- Datos diarios: un día por llamada ---

def get_heart_rate_data(client: Garmin, day: date) -> list:
    """
    Retrieve the heart rate readings of `day`.
    """

    heart_rate_data = client.get_heart_rates(day.isoformat())
    return heart_rate_data.get("heartRateValues") or []

def get_sleep_data(client: Garmin, day: date) -> dict:
    """
    Retrieve the sleep data of `day`.
    """

    return client.get_sleep_data(day.isoformat())

def get_body_battery_data(client: Garmin, day: date) -> list:
    """
    Retrieve the body battery data of `day`.
    """

    return client.get_body_battery(day.isoformat())

def get_stress_data(client: Garmin, day: date) -> dict:
    """
    Retrieve the stress data of `day`.
    """

    return client.get_stress_data(day.isoformat())

def get_daily_steps(client: Garmin, day: date) -> list:
    """
    Retrieve the steps data of `day`.
    """

    d = day.isoformat()
    return client.get_daily_steps(d, d)  # API pide inicio y fin

def get_daily_floors(client: Garmin, day: date) -> dict:
    """
    Retrieve the floors data of `day`.
    """

    return client.get_floors(day.isoformat())

# --- Rango de días: sustituye a los get_weekly_X ---

def fetch_range(
    client: Garmin,
    fetch: Callable[[Garmin, date], Any],
    start: date,
    end: date,
) -> dict[date, Any]:
    """
    Call `fetch(client, day)` for each day in [start, end].

    Returns {day: data}. Days whose request fails with a
    connection error are reported and left out. Any other
    error (a bug in our code) is raised, not hidden.
    """

    results = {}
    day = start
    while day <= end:
        try:
            results[day] = fetch(client, day)
        except GarminConnectConnectionError as e:
            print(f"{fetch.__name__} falló el {day}: {e}")
        day += timedelta(days=1)

    return results
