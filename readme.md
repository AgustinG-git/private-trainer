# Proyecto Garmin

Este proyecto conecta tu cuenta de Garmin Connect con Python para:

- consultar actividades recientes,
- extraer frecuencia cardiaca,
- filtrar carreras de la semana,
- preparar un resumen útil para un modelo de IA local con Ollama,
- y generar una recomendación de entrenamiento basada en tus datos.

La ejecución principal está en `test.py`, que autentica con Garmin, obtiene los datos, los transforma y los envía a un modelo de IA local para que genere un diagnóstico y plan de entrenamiento.

## 1. ¿Qué necesita este proyecto?

Para ejecutarlo desde cero necesitas:

- Python 3.10 o superior
- Git (opcional, pero recomendado)
- Una cuenta de Garmin Connect con datos de entrenamiento
- Ollama instalado en tu equipo
- Un modelo local descargado, por ejemplo `llama3.2`
- Un entorno virtual de Python

## 2. Estructura del proyecto

```text
00.Proyecto_Garmin/
├── .env                  # Credenciales locales de Garmin (NO subir a Git)
├── .venv                 # Entorno virtual de Python (puedes crear uno tú)
├── agents/
│   └── ollama_agents.py  # Llama al modelo local de Ollama
├── utils/
│   ├── garmin_utils.py   # Funciones para autenticación y consultas a Garmin
│   ├── data_merger.py    # Filtrado y transformación de carreras
│   └── visuals.py        # Gráficos de frecuencia cardiaca
├── test.py               # Script principal que ejecuta el flujo completo
├── requirements.txt      # Dependencias del proyecto
├── readme.md             # Documentación del proyecto
└── LICENSE               # Licencia
```

## 3. Requisitos previos

### 3.1 Instalar Python

Descarga e instala Python 3.10+ desde:

https://www.python.org/downloads/

Durante la instalación asegúrate de marcar la opción:

- Add Python to PATH

### 3.2 Instalar Ollama

Instala Ollama desde:

https://ollama.com/download

Una vez instalado, descarga el modelo que usa el proyecto:

```powershell
ollama pull llama3.2
```

Y asegúrate de que el servicio de Ollama esté corriendo:

```powershell
ollama serve
```

> Si vas a usar este proyecto desde Windows, normalmente basta con que Ollama esté instalado y el modelo descargado. El proyecto usa `langchain_ollama` y el nombre por defecto del modelo es `llama3.2`.

## 4. Clonar o abrir el proyecto

Desde una terminal, entra en la carpeta del proyecto. Si lo tienes clonado, por ejemplo:

```powershell
cd C:\Users\tu_usuario\Documents\Machine Learning\00.Proyecto_Garmin
```

## 5. Crear el entorno virtual

En Windows:

```powershell
py -m venv .venv
```

Activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea scripts, ejecuta esto antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego repite la activación.

## 6. Instalar dependencias

Con el entorno virtual activado, instala las librerías necesarias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si prefieres instalar las dependencias manualmente, puedes hacerlo con:

```powershell
pip install garminconnect python-dotenv matplotlib langchain langchain-ollama
```

## 7. Crear el archivo `.env`

En la raíz del proyecto crea un archivo llamado `.env` con estas variables:

```dotenv
GARMIN_EMAIL=tu_correo@ejemplo.com
GARMIN_PASSWORD=tu_contrasena
```

Ejemplo real:

```dotenv
GARMIN_EMAIL=juan.perez@gmail.com
GARMIN_PASSWORD=MiPasswordSecreta123
```

Importante:

- no compartas este archivo,
- no lo subas a GitHub,
- usa tus credenciales reales de Garmin Connect.

El código carga estas variables con `python-dotenv` y `os.getenv()`.

## 8. Verificar que Ollama esté listo

Antes de ejecutar la app, comprueba que el modelo esté disponible:

```powershell
ollama list
```

Debe aparecer `llama3.2` o el modelo que hayas descargado.

## 9. Ejecutar el proyecto

Desde la carpeta del proyecto, con el entorno virtual activado:

```powershell
python test.py
```

Eso hará lo siguiente:

1. carga las variables del `.env`,
2. inicia sesión en Garmin Connect,
3. obtiene actividades recientes,
4. filtra las carreras de la semana,
5. consulta la IA local de Ollama,
6. genera un diagnóstico y plan de entrenamiento.

## 10. ¿Qué hace exactamente `test.py`?

El script principal importa:

- `load_dotenv()` para leer `.env`,
- `garmin_client()` para autenticarse con Garmin,
- `parse_weekly_activities()` para limpiar los datos,
- `chat_Ollama()` para enviar el análisis a Ollama.

Luego hace una llamada como esta:

```python
weekly_activities = parse_weekly_activities(client)
print(chat_Ollama(..., modelo="llama3.2"))
```

Es decir, envía a la IA una descripción de tus carreras de la semana y pide un plan de entrenamiento.

## 11. Solución de problemas comunes

### Error: `GARMIN_PASSWORD` no está definido

Esto sucede porque intentas usar una variable de entorno como si fuera una variable normal de Python. La forma correcta es:

```python
import os
password = os.getenv("GARMIN_PASSWORD")
```

### Error: `Connection failed` o no se conecta a Garmin

Revisa:

- que `GARMIN_EMAIL` y `GARMIN_PASSWORD` sean correctos,
- que la cuenta de Garmin tenga acceso a la app,
- que el entorno virtual esté activo,
- que `garminconnect` esté instalado correctamente.

### Error: no hay modelo de Ollama disponible

Ejecuta:

```powershell
ollama pull llama3.2
```

Y luego:

```powershell
ollama serve
```

### El programa no encuentra el módulo `utils`

Asegúrate de ejecutar el script desde la raíz del proyecto y no desde otra carpeta. Por ejemplo:

```powershell
cd C:\Users\tu_usuario\Documents\Machine Learning\00.Proyecto_Garmin
python test.py
```

## 12. Flujo recomendado de uso

Para una experiencia limpia, sigue este orden:

```powershell
# 1. Entrar al proyecto
cd C:\Users\tu_usuario\Documents\Machine Learning\00.Proyecto_Garmin

# 2. Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Crear .env con tus credenciales
notepad .env

# 5. Verificar Ollama
ollama pull llama3.2
ollama list

# 6. Ejecutar
python test.py
```

## 13. Recomendaciones importantes

- Mantén tu archivo `.env` local y no lo compartas.
- Si cambias de modelo de Ollama, ajusta el parámetro `modelo` en `test.py`.
- Si no quieres usar Ollama, tendrías que adaptar el código para usar otra API o proveedor de IA.
- Este proyecto está pensado para análisis personal y entrenamiento deportivo, no para automatizar tareas de terceros ni extraer datos de personas sin su consentimiento.

## 14. Resumen rápido

Si quieres arrancar en 30 segundos:

```powershell
cd C:\Users\tu_usuario\Documents\Machine Learning\00.Proyecto_Garmin
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
notepad .env
python test.py
```

Y en `.env`:

```dotenv
GARMIN_EMAIL=tu_correo
GARMIN_PASSWORD=tu_contrasena
```

## 15. Nota final

Este proyecto combina tres piezas principales:

- Garmin Connect: extracción de datos reales,
- Python: limpieza y preparación de datos,
- Ollama: análisis inteligente del entrenamiento.

Si sigues estos pasos, cualquier persona con conocimientos básicos de Python puede arrancar el proyecto desde cero y ejecutarlo correctamente en su equipo.

- `get_weekly_activities(client)` reutiliza una sesion existente.
- `parse_weekly_runs` filtra carreras mediante `activityType.typeKey`.
- `parse_weekly_activities` devuelve una estructura resumida bajo la clave `weekly_runs`.
- `get_heart_rate_data(client)` devuelve las lecturas de hoy.
- `heartRateValues` contiene pares de timestamp y pulsaciones.
- Matplotlib permite transformar esos datos en una grafica.
