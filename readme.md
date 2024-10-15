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
Una vez instalado levantar el server con `flask run`

### Docker
Ejecutar los siguientes comandos desde la raíz del proyecto.
`./build.sh`: construye la imagen. Solo es necesario ejecutarlo una vez.
`./start.sh`: ejecutar un contenedor con la API. 