from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config
from app.routes import auth

app = FastAPI(title="Now Listening API", version="0.1")

origins = [
    Config.ORIGINS # todo: replace this with domain specified in .env
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "status": "running"
    }