from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import prendas  # Importamos nuestro nuevo router

app = FastAPI(
    title="Sistema de Gestión de Inventario",
    description="API para el control de stock de prendas de vestir",
    version="1.0.0"
)

# Configuración de CORS profesional para conectar con Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se restringe al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de ciclo de vida para inicializar la base de datos al arrancar
@app.on_event("startup")
def on_startup():
    init_db()

# Incluimos las rutas del módulo de prendas
app.include_router(prendas.router)

@app.get("/")
def home():
    return {"status": "Stock API is running", "orm": "SQLModel"}