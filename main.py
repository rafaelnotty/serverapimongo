from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

USER_MONGODB = os.getenv("USER_MONGODB")
PASS_MONGODB = os.getenv("PASS_MONGODB")
from pydantic import BaseModel

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

##revisar como activar un healthcheck: en el .yml

import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("La dirección IP del servidor es:", local_ip)

class presiones(BaseModel):
    DateTime_dev: str
    device: str
    value: float
    

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las conexiones
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar la carpeta de templates
templates = Jinja2Templates(directory="templates")

uri = "mongodb+srv://rafaelnotty:AdminRrrrr100589@myprojecta.jdb5vhu.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['myprojectrr2']
collection = db['preassure_sensors2']
    
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Retornar el archivo HTML
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/enviar_datos/")
async def recibir_datos(datetime1: str, pres_alm: float):
    # Convertir datetime1 y datetime2 a objetos datetime si es necesario
    datetime1 = datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S")
    
    # Aquí procesarías los datos recibidos como prefieras
    return {"datetime1": datetime1, "pres_alm": pres_alm}
    
# Endpoint para crear un registro de presiones
@app.post("/presiones/")
async def create_presion(presion_data: dict):
    try:
        #presion_dict = presion.model_dump()
        #result = collection.insert_one(presion_dict)
        #presion_dict["_id"] = str(result.inserted_id)
        #return presion_dict
        result = collection.insert_one(presion_data)
        presion_data["_id"] = str(result.inserted_id)
        return presion_data
    except PyMongoError as e:
        print(f"Ha ocurrido un error en la conexión a la BD: {e}")
        return None

    #except:
    #    print("Ha ocurrido un error en la conexión a la BD")


@app.get("/health")
async def health_check(request: Request):
    # Aquí puedes incluir lógicas de comprobación, como verificar conexiones a la base de datos

    operativo = True   
    status_message = "Operativo" if operativo else "NO Operativo"

    # Renderizar la plantilla con el estado
    return templates.TemplateResponse("health_status.html", {"request": request, "status": status_message})

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
