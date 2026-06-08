import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@database_postgres:5432/stock_db")

# Cambiamos esta línea para agregar tolerancia a la conexión en Docker
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # Verifica si la conexión sigue viva antes de usarla
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()