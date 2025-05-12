## DP - Detección con NLP

Detección de dark patterns usando NLP

### Confirmshaming

Detecta el DP Confirmshaming en fragmentos de texto.

```plaintext
POST /shaming
```

Atributos requeridos:

| Atributo              | Tipo                  | Descripción           |
|-----------------------|-----------------------|-----------------------|
| `tokens`              | Lista de diccionarios | Cada diccionario de la lista tiene el texto y xPath de un elemento DOM particular. |
| `tokens[].text`       | string                | Texto del elemento a analizar. |
| `tokens[].path`       | lista de strings      | xPath que apunta a la ubicación exacta del elemento dentro del DOM. |

Retorna una **lista** con:

| Atributo            | Tipo             | Descripción           |
|---------------------|------------------|-----------------------|
| `[].text`              | string           | Texto que contiene un DP. |
| `[].path`              | lista de strings | xPath que apunta a la ubicación exacta del elemento que tiene un DP dentro del DOM. |
| `[].pattern`           | string           | String identificador del tipo de DP |

Ejemplo del body de un request:

```json
{
    "tokens": [
        {
            "text": "No me gusta ahorrar",
            "path": [".//div[1]/div[4]/aside[1]/section[1]/div[1]"]
        }
    ]
}
```

Ejemplo de la respuesta:

```json
[
    {
        "text": "No me gusta ahorrar"
        "path": [".//div[1]/div[4]/aside[1]/section[1]/div[1]"],
        "pattern": "SHAMING"
    }
]
```

### Fake Urgency

Detecta el DP Fake Urgency en fragmentos de texto.

```plaintext
POST /urgency
```
> [!NOTE]
> El request y response siguen el mismo esquema que Confirmshaming. Ver los ejemplos de arriba.


## Test de Spacy para confirmshaming
### Instalación

> [!CAUTION]
> Instalar en un virtual enviroment para no romper todo.

Crear un entorno e instalar las dependencias con:
```
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
En windows:
```
python -m venv .env
.\.env\Scripts\activate
pip install -r requirements.txt
```
Una vez instalado levantar el server con `flask run`

### Docker
Ejecutar los siguientes comandos desde la raíz del proyecto.
`./build.sh`: construye la imagen. Solo es necesario ejecutarlo una vez.
`./start.sh`: ejecutar un contenedor con la API. 
