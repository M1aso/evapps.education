from fastapi import FastAPI
import os
from .api import router as analytics_router

ROOT_PATH = os.getenv("ROOT_PATH", "")
app = FastAPI(
    title="Analytics Service",
    root_path=ROOT_PATH,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
app.include_router(analytics_router)
