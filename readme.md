# Guía de estudio: biblioteca `garminconnect`

Esta guía resume lo aprendido al conectar Python con Garmin Connect, consultar actividades y representar la frecuencia cardiaca con una gráfica.

## 1. Estructura del proyecto

```text
00.Proyecto_Garmin/
├── .env              # Credenciales locales, no debe compartirse
├── garmin_utils.py   # Funciones reutilizables para Garmin
├── test.py           # Script principal de prueba
└── readme.md         # Esta guía
```

La idea es separar la lógica reutilizable (`garmin_utils.py`) del archivo que ejecuta el programa (`test.py`).

## 2. Instalación

El proyecto utiliza un entorno virtual. Con el entorno activado, instala las dependencias:

```powershell
pip install garminconnect python-dotenv matplotlib
```

También es recomendable guardar las dependencias:

```powershell
pip freeze > requirements.txt
```

## 3. Variables de entorno

El archivo `.env` se encuentra en la raíz del proyecto y contiene los nombres esperados por el código:

```dotenv
GARMIN_EMAIL=tu_correo
GARMIN_PASSWORD=tu_contraseña
```

No se deben escribir las credenciales directamente en el código ni subir `.env` a Git.

Para leerlas:

```python
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
```

### Idea importante

`load_dotenv()` carga los valores en las variables de entorno del proceso. No crea automáticamente una variable Python llamada `GARMIN_PASSWORD`.

Por eso esto produce un error:

```python
print(GARMIN_PASSWORD)
```

La forma correcta es utilizar `os.getenv`:

```python
print(os.getenv("GARMIN_PASSWORD"))
```

En un programa real no conviene imprimir una contraseña. Para comprobar si se ha cargado, se puede mostrar únicamente un indicador:

```python
print("Contraseña cargada:", os.getenv("GARMIN_PASSWORD") is not None)
```

## 4. Crear el cliente y autenticarse

La clase principal es `Garmin`:

```python
from garminconnect import Garmin

client = Garmin(email, password)
client.login("~/.garminconnect")
```

El objeto `client` representa la conexión con Garmin Connect y se pasa a las funciones que necesitan consultar datos.

En este proyecto, `connection_test()` intenta iniciar sesión, muestra si la conexión ha sido correcta y devuelve `True` o `False`:

```python
from garmin_utils import connection_test

if connection_test():
	print("La conexión está lista para consultar datos")
```

## 5. Consultar actividades por fechas

La biblioteca permite consultar actividades mediante `get_activities_by_date(start, end)`. Las fechas se envían como texto con formato ISO: `YYYY-MM-DD`.

Ejemplo para el mes actual:

```python
from datetime import date

today = date.today().isoformat()
first_day = date.today().replace(day=1).isoformat()
activities = client.get_activities_by_date(first_day, today)
```

En `garmin_utils.py` se han creado dos funciones:

- `get_monthly_activities()`: devuelve las actividades desde el primer día del mes hasta hoy.
- `get_weekly_activities()`: devuelve las actividades de los últimos siete días hasta hoy.

Uso desde `test.py`:

```python
from garmin_utils import get_monthly_activities, get_weekly_activities

monthly_activities = get_monthly_activities()
weekly_activities = get_weekly_activities()

print("Actividades del mes:", len(monthly_activities))
print("Actividades de la semana:", len(weekly_activities))
```

El resultado es una lista de diccionarios. Para estudiarlo sin perder contexto, es preferible imprimir un resumen con etiquetas y totales antes que imprimir listas sin identificar.

## 6. Consultar la frecuencia cardiaca

Para obtener las pulsaciones de un día se utiliza `get_heart_rates(fecha)`:

```python
today = date.today().isoformat()
heart_rate_data = client.get_heart_rates(today)
```

La respuesta contiene, entre otros datos, `heartRateValues`. Cada lectura se representa como un par:

```python
[timestamp, heart_rate]
```

Algunas respuestas pueden contener valores `None`, por lo que hay que filtrarlos antes de convertirlos o representarlos:

```python
readings = heart_rate_data.get("heartRateValues", [])

for timestamp, heart_rate in readings:
	if timestamp is None or heart_rate is None:
		continue
	print(timestamp, heart_rate)
```

## 7. Convertir timestamps y dibujar la gráfica

La función `plot_today_heart_rates(garmin_client)` reúne todo el proceso:

1. Calcula la fecha de hoy.
2. Pide los datos a Garmin.
3. Extrae `heartRateValues`.
4. Descarta lecturas incompletas.
5. Convierte el timestamp a una fecha y hora.
6. Dibuja las pulsaciones con Matplotlib.
7. Devuelve la figura.

Los timestamps pueden llegar en segundos o en milisegundos. La función detecta los valores grandes y divide por `1000` cuando es necesario:

```python
if timestamp > 10**12:
	timestamp /= 1000
```

La función se utiliza así:

```python
import matplotlib.pyplot as plt
from garmin_utils import plot_today_heart_rates

heart_rate_figure = plot_today_heart_rates(client)
plt.show()
```

La figura también se puede guardar en un archivo:

```python
heart_rate_figure.savefig("frecuencia_cardiaca_hoy.png")
```

La etiqueta `bpm` significa *beats per minute*, es decir, pulsaciones por minuto.

## 8. Flujo completo del programa

El flujo actual de `test.py` es:

```python
load_dotenv()
client = Garmin(os.getenv("GARMIN_EMAIL"), os.getenv("GARMIN_PASSWORD"))
client.login("~/.garminconnect")

monthly_activities = get_monthly_activities()
weekly_activities = get_weekly_activities()

heart_rate_figure = plot_today_heart_rates(client)
plt.show()
```

Observa que `get_monthly_activities()` y `get_weekly_activities()` crean su propio cliente y vuelven a autenticarse, mientras que la gráfica recibe el cliente ya creado como argumento. Una mejora futura sería reutilizar el mismo cliente en todas las funciones para evitar conexiones repetidas.

## 9. Errores habituales

### `NameError: name 'GARMIN_PASSWORD' is not defined`

Significa que se ha usado el nombre de una variable de entorno como si fuera una variable Python. Solución:

```python
password = os.getenv("GARMIN_PASSWORD")
```

### El valor es `None`

Comprueba que:

- El archivo se llama exactamente `.env`.
- Está en la carpeta desde la que se ejecuta el programa.
- La clave coincide exactamente con `GARMIN_PASSWORD` o `GARMIN_EMAIL`.
- No hay espacios innecesarios alrededor del nombre.
- Se ha ejecutado `load_dotenv()` antes de llamar a `os.getenv`.

### No aparecen puntos en la gráfica

Puede que Garmin no haya devuelto lecturas para la fecha consultada. La función maneja este caso mostrando un mensaje dentro de la gráfica.

### No se debe compartir información sensible

Nunca publiques el contenido de `.env`, contraseñas, tokens ni archivos de sesión de Garmin. Si una credencial se expone, debe cambiarse cuanto antes.

## 10. Ejercicios de estudio

1. Modifica la gráfica para mostrar una línea horizontal con la frecuencia cardiaca en reposo.
2. Añade una función que devuelva el valor máximo y mínimo de pulsaciones del día.
3. Guarda automáticamente la gráfica con la fecha en el nombre del archivo.
4. Cambia `get_monthly_activities()` para que reciba una fecha inicial y una fecha final como argumentos.
5. Reutiliza un único objeto `Garmin` en todas las consultas.
6. Añade comprobaciones que indiquen claramente si falta `GARMIN_EMAIL` o `GARMIN_PASSWORD`.

## Resumen

Los conceptos principales aprendidos son:

- Las variables de `.env` se leen con `os.getenv` después de ejecutar `load_dotenv()`.
- `Garmin(email, password)` crea el cliente.
- `login()` autentica la sesión.
- Las consultas por fecha utilizan textos con formato `YYYY-MM-DD`.
- Las actividades se consultan con `get_activities_by_date`.
- La frecuencia cardiaca se consulta con `get_heart_rates`.
- `heartRateValues` contiene pares de timestamp y pulsaciones.
- Matplotlib permite transformar esos datos en una gráfica.
