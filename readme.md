# Guia de estudio: biblioteca `garminconnect`

Esta guia resume lo aprendido al conectar Python con Garmin Connect, organizar el codigo en modulos, consultar actividades y frecuencia cardiaca, filtrar carreras y preparar visualizaciones.

## 1. Estructura del proyecto

```text
00.Proyecto_Garmin/
|-- .env                  # Credenciales locales, no debe compartirse
|-- test.py               # Script principal de prueba
|-- readme.md             # Esta guia
`-- utils/
    |-- garmin_utils.py   # Cliente Garmin y consultas de datos
    |-- data_merger.py    # Filtrado y transformacion de actividades
    `-- visuals.py        # Graficas
```

La idea es separar la obtencion de datos, la transformacion y la presentacion. `test.py` coordina estas piezas.

## 2. Instalacion

El proyecto utiliza un entorno virtual. Con el entorno activado, instala las dependencias:

```powershell
pip install garminconnect python-dotenv matplotlib
```

Tambien es recomendable guardar las dependencias:

```powershell
pip freeze > requirements.txt
```

## 3. Variables de entorno

El archivo `.env` se encuentra en la raiz del proyecto y contiene los nombres esperados por el codigo:

```dotenv
GARMIN_EMAIL=tu_correo
GARMIN_PASSWORD=tu_contrasena
```

No se deben escribir las credenciales directamente en el codigo ni subir `.env` a Git.

Para leerlas:

```python
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
```

### Idea importante

`load_dotenv()` carga los valores en las variables de entorno del proceso. No crea automaticamente una variable Python llamada `GARMIN_PASSWORD`.

Por eso esto produce un error:

```python
print(GARMIN_PASSWORD)
```

La forma correcta es utilizar `os.getenv`:

```python
print(os.getenv("GARMIN_PASSWORD"))
```

En un programa real no conviene imprimir una contrasena. Para comprobar si se ha cargado, muestra solo un indicador:

```python
print("Contrasena cargada:", os.getenv("GARMIN_PASSWORD") is not None)
```

## 4. Crear el cliente y autenticarse

La clase principal es `Garmin`:

```python
from garminconnect import Garmin

client = Garmin(email, password)
client.login("~/.garminconnect")
```

El objeto `client` representa la conexion con Garmin Connect y se pasa a las funciones que necesitan consultar datos.

En la version actual, `utils/garmin_utils.py` contiene `garmin_client()`. Esta funcion crea el cliente, intenta iniciar sesion y devuelve el objeto conectado:

```python
from utils.garmin_utils import garmin_client

client = garmin_client()
if client:
    print("La conexion esta lista para consultar datos")
```

Si el inicio de sesion falla, la funcion imprime el error y devuelve `False`. Centralizar la autenticacion permite reutilizar la misma sesion.

## 5. Consultar actividades por fechas

La biblioteca permite consultar actividades mediante `get_activities_by_date(start, end)`. Las fechas se envian como texto con formato ISO: `YYYY-MM-DD`.

Ejemplo para el mes actual:

```python
from datetime import date

today = date.today().isoformat()
first_day = date.today().replace(day=1).isoformat()
monthly_activities = client.get_activities_by_date(first_day, today)
```

En `utils/garmin_utils.py`, `get_weekly_activities(client)` recibe un cliente ya autenticado y devuelve las actividades de los ultimos siete dias:

```python
from utils.garmin_utils import get_weekly_activities

weekly_activities = get_weekly_activities(client)
print("Actividades de la semana:", len(weekly_activities))
```

El resultado de `get_activities_by_date` es una lista de diccionarios. Para estudiarlo sin perder contexto, es preferible imprimir un resumen con etiquetas y totales:

```python
print("\n=== Actividades de los ultimos 7 dias ===")
print(f"Total de actividades: {len(weekly_activities)}")
print(weekly_activities)
```

Pasar `client` como argumento evita autenticar una vez por cada consulta.

## 6. Consultar y preparar la frecuencia cardiaca

En `utils/garmin_utils.py`, `get_heart_rate_data(client)` hace la consulta de hoy y devuelve directamente la lista `heartRateValues`:

```python
from utils.garmin_utils import get_heart_rate_data

readings = get_heart_rate_data(client)
```

La respuesta original de Garmin contiene, entre otros datos, `heartRateValues`. Cada lectura se representa como un par:

```python
[timestamp, heart_rate]
```

Algunas respuestas pueden contener valores `None`, por lo que hay que filtrarlos antes de convertirlos o representarlos:

```python
for timestamp, heart_rate in readings:
    if timestamp is None or heart_rate is None:
        continue
    print(timestamp, heart_rate)
```

## 7. Convertir timestamps y dibujar la grafica

La funcion `plot_today_heart_rates()` de `utils/visuals.py` reune todo el proceso:

1. Calcula la fecha de hoy.
2. Pide los datos a Garmin.
3. Extrae `heartRateValues` mediante `get_heart_rate_data`.
4. Descarta lecturas incompletas.
5. Convierte el timestamp a fecha y hora.
6. Dibuja las pulsaciones con Matplotlib.
7. Devuelve la figura.

Los timestamps pueden llegar en segundos o en milisegundos. La conversion para milisegundos es:

```python
if timestamp > 10**12:
    timestamp /= 1000
```

Uso:

```python
import matplotlib.pyplot as plt
from utils.visuals import plot_today_heart_rates

heart_rate_figure = plot_today_heart_rates()
plt.show()
```

La figura tambien se puede guardar:

```python
heart_rate_figure.savefig("frecuencia_cardiaca_hoy.png")
```

La etiqueta `bpm` significa *beats per minute*, es decir, pulsaciones por minuto.

## 8. Filtrar y transformar carreras

`utils/data_merger.py` convierte la respuesta completa de Garmin en una estructura mas pequena y facil de analizar.

### Filtrar carreras

`parse_weekly_runs(weekly_runs)` recorre las actividades y conserva aquellas cuyo `activityType.typeKey` contiene `running`. Esto incluye carreras normales y carreras en cinta (`treadmill_running`).

```python
run_type = run.get("activityType", {}).get("typeKey", "")
if "running" in run_type:
    # La actividad se transforma en un diccionario resumido
```

El uso de `.get()` evita errores cuando falta una clave:

```python
name = run.get("activityName", "Carrera")
distance = run.get("distance", 0)
average_heart_rate = run.get("averageHR", 0)
```

### Estructura resumida de una carrera

Cada carrera filtrada conserva estas categorias:

- Identidad: `name`, `date`.
- Volumen: `distance_meters`, `duration_seconds`.
- Intensidad: `average_heart_rate`, `training_load`.
- Dinamica: `cadence`, `stride_length_cm`, `vertical_oscillation_cm`, `vertical_ratio`.
- Zonas cardiacas: `zone_1`, `zone_2`, `zone_3`, `zone_4`, `zone_5`.

`parse_weekly_activities(client)` combina la consulta semanal con el filtrado y devuelve un diccionario bajo la clave `weekly_runs`:

```python
{
    "weekly_runs": [
        {
            "name": "Carrera",
            "distance_meters": 5000,
            "average_heart_rate": 145
        }
    ]
}
```

Ejemplo de uso:

```python
from utils.data_merger import parse_weekly_activities

parsed_data = parse_weekly_activities(client)
runs = parsed_data["weekly_runs"]
print("Carreras encontradas:", len(runs))
```

## 9. Flujo recomendado del programa

El flujo recomendado es autenticar una vez, reutilizar `client`, obtener los datos originales, transformarlos y finalmente visualizarlos:

```python
import matplotlib.pyplot as plt

from utils.data_merger import parse_weekly_activities
from utils.garmin_utils import garmin_client, get_weekly_activities
from utils.visuals import plot_today_heart_rates

client = garmin_client()
if client:
    weekly_activities = get_weekly_activities(client)
    parsed_data = parse_weekly_activities(client)
    heart_rate_figure = plot_today_heart_rates()
    plt.show()
```

## 10. Errores habituales y puntos pendientes

### `NameError: name 'GARMIN_PASSWORD' is not defined`

Significa que se ha usado el nombre de una variable de entorno como si fuera una variable Python. Solucion:

```python
password = os.getenv("GARMIN_PASSWORD")
```

### El valor es `None`

Comprueba que:

- El archivo se llama exactamente `.env`.
- Esta en la carpeta desde la que se ejecuta el programa.
- La clave coincide exactamente con `GARMIN_PASSWORD` o `GARMIN_EMAIL`.
- No hay espacios innecesarios alrededor del nombre.
- Se ha ejecutado `load_dotenv()` antes de llamar a `os.getenv`.

### No aparecen puntos en la grafica

Puede que Garmin no haya devuelto lecturas para la fecha consultada. La funcion maneja este caso mostrando un mensaje dentro de la grafica.

### Import duplicado en `test.py`

No se debe importar `get_weekly_activities` desde dos sitios. La importacion recomendada es:

```python
from utils.garmin_utils import get_weekly_activities
from utils.data_merger import parse_weekly_activities
```

`data_merger.py` utiliza la funcion de consulta, pero no debe reemplazarla con otro nombre.

### Import de la grafica

`utils/visuals.py` debe importar el modulo desde el paquete del proyecto:

```python
from utils.garmin_utils import get_heart_rate_data
```

Asi se evita depender de un `garmin_utils.py` situado en la raiz.

### No se debe compartir informacion sensible

Nunca publiques el contenido de `.env`, contrasenas, tokens ni archivos de sesion de Garmin. Si una credencial se expone, debe cambiarse cuanto antes.

## 11. Ejercicios de estudio

1. Modifica la grafica para mostrar una linea horizontal con la frecuencia cardiaca en reposo.
2. Anade una funcion que devuelva el valor maximo y minimo de pulsaciones del dia.
3. Guarda automaticamente la grafica con la fecha en el nombre del archivo.
4. Cambia la consulta mensual para que reciba una fecha inicial y una fecha final como argumentos.
5. Reutiliza un unico objeto `Garmin` en todas las consultas.
6. Anade comprobaciones que indiquen claramente si falta `GARMIN_EMAIL` o `GARMIN_PASSWORD`.
7. Calcula la distancia total y el tiempo total de las carreras de la semana.
8. Convierte `distance_meters` a kilometros y `duration_seconds` a minutos.
9. Crea una grafica del ritmo medio de cada carrera.
10. Corrige los imports del paquete `utils` y prueba el flujo completo desde `test.py`.

## 12. Resumen

Los conceptos principales aprendidos son:

- Las variables de `.env` se leen con `os.getenv` despues de ejecutar `load_dotenv()`.
- `Garmin(email, password)` crea el cliente.
- `login()` autentica la sesion.
- Las consultas por fecha utilizan textos con formato `YYYY-MM-DD`.
- Las actividades se consultan con `get_activities_by_date`.
- `garmin_client()` centraliza la creacion y autenticacion del cliente.
- `get_weekly_activities(client)` reutiliza una sesion existente.
- `parse_weekly_runs` filtra carreras mediante `activityType.typeKey`.
- `parse_weekly_activities` devuelve una estructura resumida bajo la clave `weekly_runs`.
- `get_heart_rate_data(client)` devuelve las lecturas de hoy.
- `heartRateValues` contiene pares de timestamp y pulsaciones.
- Matplotlib permite transformar esos datos en una grafica.
