from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.users import users  
from app.routers.image_files import router as image_files  
from app.routers.analysis_results import router as anylisis  
from app.config import settings

ROUTER_PREFIX = "/api/v1"
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para materia de IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción pon dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    users,
    prefix=ROUTER_PREFIX, 
    tags=["Users"]     
)

app.include_router(
    image_files,
    prefix=ROUTER_PREFIX, 
    tags=["Imágenes"]     
)
app.include_router(
    anylisis,
    prefix=ROUTER_PREFIX, 
    tags=["Analisis"]     
)

@app.get("/")
def root():
    return {
        "message": "online",
        "Usuarios":"/api/v1/users",
        "Imagenes":"/api/v1/image_files",
        "Análisis":"/api/v1/analysis_results",
    }

