## DP - Detección con NLP

Proyecto para detectar algunos "dark patterns" (confirmshaming, fake urgency, scarcity) usando NLP.

Este repositorio expone una pequeña API Flask con los siguientes endpoints principales:

- POST /shaming    -> Detecta Confirmshaming (confirm-shaming)
- POST /urgency    -> Detecta Fake Urgency
- POST /scarcity   -> Detecta patrones de escasez

Archivo principal: `app.py` (levanta la app Flask). El Dockerfile expone el puerto 5000 y el comando por defecto es `flask run --host=0.0.0.0`.

---

## Endpoints y ejemplos

1) /shaming

Request: JSON con un campo `tokens` (lista de objetos {text, path}).

Ejemplo request:

```json
{
    "tokens": [
        {"text": "No me gusta ahorrar", "path": [".//div[1]/div[4]/aside[1]/section[1]/div[1]"]}
    ]
}
```

Ejemplo response (lista de instancias detectadas):

```json
[
    {"text": "No me gusta ahorrar", "path": [".//div[1]/..."], "pattern": "SHAMING"}
]
```

2) /urgency

Request/response siguen el mismo esquema de `shaming` en la mayoría de los casos; también existe validación con esquemas (`UrgencyRequestSchema`).

3) /scarcity

Este endpoint acepta un JSON siguiendo `ScarcityRequestSchema` y devuelve un objeto con `instances` indicando `has_scarcity` por texto.

Ejemplo request (simplificado):

```json
{
    "version": "1.0",
    "texts": [
        {"text": "Solo quedan 3 unidades!", "path": "/producto/123", "id": "e1"},
        {"text": "Oferta limitada", "path": "/promociones/oferta"}
    ]
}
```

Ejemplo response:

```json
{
    "version": "1.0",
    "instances": [
        {"text": "Solo quedan 3 unidades!", "path": "/producto/123", "id": "e1", "has_scarcity": true},
        {"text": "Oferta limitada", "path": "/promociones/oferta", "has_scarcity": false}
    ]
}
```

---

## Instalación local (virtualenv)

Se recomienda usar un entorno virtual por separado.

Linux / macOS:

```bash
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
flask run
```

Windows (PowerShell):

```powershell
python -m venv .env
.\.env\Scripts\Activate.ps1
pip install -r requirements.txt
flask run
```

Nota: las dependencias incluyen modelos de spaCy grandes y paquetes para transformers/torch; la instalación puede ser lenta y consumir mucho espacio. Si no quieres instalar todo localmente, usa Docker (siguientes secciones).

---

## Docker (recomendado)

El repositorio ya incluye un `Dockerfile` y scripts `build.sh`, `start.sh`, `build.ps1`, `start.ps1`.

Nombre de la imagen usada por los scripts: `jcgardey/dark-patterns-extension-api`.

Construir la imagen (PowerShell):

```powershell
.\build.ps1
# ó explícito
docker build -t jcgardey/dark-patterns-extension-api .
```

Arrancar un contenedor (PowerShell):

```powershell
.\start.ps1
# ó explícito
docker run -p 5000:5000 -v ${PWD}:/usr/src/app jcgardey/dark-patterns-extension-api
```

Si prefieres una ejecución más controlada (contenedor nombrado, reinicio automático, detached):

```powershell
docker build -t dark-patterns-back .
docker run --name dark-patterns-back -p 5000:5000 --restart unless-stopped -d dark-patterns-back
docker logs -f dark-patterns-back
```

Para detener y eliminar el contenedor:

```powershell
docker stop dark-patterns-back; docker rm dark-patterns-back
```

Si quieres montar el código en caliente para desarrollo (no recomendado en producción):

```powershell
docker run --name dark-patterns-back -p 5000:5000 -v ${PWD}:/usr/src/app -w /usr/src/app --restart unless-stopped -d jcgardey/dark-patterns-extension-api
```

---

## Tests

Hay un archivo `test_api.py` en el repo. Ejecuta las pruebas con pytest:

```powershell
pip install -r requirements.txt
pytest -q
```

---

## Notas y troubleshooting

- Asegúrate de que Docker Desktop esté en marcha en Windows antes de ejecutar comandos Docker.
- Si recibes errores relacionados con spaCy models, instala los modelos requeridos (o usa la imagen Docker, que ya instala desde `requirements.txt`).
- El servicio escucha en el puerto 5000 por defecto.

--- 
