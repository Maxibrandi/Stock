from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel
from typing import List
from contextlib import asynccontextmanager
from routes import prendas, movimientos, ventas, auth, reportes

# Importamos la base de datos, modelos y routers
from models.bd import get_db, engine, Rol, Usuario
from routes import prendas, movimientos, ventas, auth

# --- 1. LÓGICA DE INICIALIZACIÓN (LIFESPAN) ---

def inicializar_roles_por_defecto():
    """Crea los roles iniciales si la base de datos está limpia"""
    with Session(engine) as session:
        # Traemos todos los roles de la base de datos
        roles = session.exec(select(Rol)).all()

        # Si la lista está vacía, insertamos los roles por defecto
        if not roles:
            admin = Rol(nombre_rol="Administrador", puede_ver_ganancias=True)
            vendedor = Rol(nombre_rol="Vendedor", puede_ver_ganancias=False)
            session.add(admin)
            session.add(vendedor)
            session.commit()
            print("Roles 'Administrador' (ID 1) y 'Vendedor' (ID 2) creados con éxito.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar el servidor creamos las tablas y cargamos datos semilla
    SQLModel.metadata.create_all(engine)
    inicializar_roles_por_defecto()
    yield

# --- 2. INICIALIZACIÓN DE LA APP ÚNICA ---
app = FastAPI(title="Sistema de Gestión de Stock", lifespan=lifespan)

# --- 3. CONFIGURACIÓN DE CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. ROUTER LOCAL (Para endpoints definidos en este mismo archivo) ---
router = APIRouter()

@app.get("/")
def home():
    return {"status": "Stock API is running with Database and CORS enabled"}

@router.get("/api/roles/", response_model=List[Rol])
def listar_roles(db: Session = Depends(get_db)):
    return db.exec(select(Rol)).all()

@router.post("/api/roles/", response_model=Rol)
def crear_rol(rol: Rol, db: Session = Depends(get_db)):
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

# --- 5. INCLUSIÓN DE TODOS LOS ROUTERS ---
app.include_router(auth.router)
app.include_router(prendas.router)
app.include_router(movimientos.router)
app.include_router(ventas.router)
app.include_router(reportes.router)
app.include_router(router)  # Incluye /api/roles/