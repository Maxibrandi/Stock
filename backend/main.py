from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
async def get_data():
    return {"items": ["Vue", "FastAPI", "uv"]}

@app.get("/test")
async def test():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"status": "Stock API is running"}