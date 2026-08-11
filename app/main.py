# app/main.py
from fastapi import FastAPI

from app.presentation.routers import router as main_router

app = FastAPI()

app.include_router(main_router)
