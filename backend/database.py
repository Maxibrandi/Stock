import os
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stock_user:stock_password@db:5432/stock_inventory")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session