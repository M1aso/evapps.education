from fastapi import FastAPI
import os
from .api import router as analytics_router

ROOT_PATH = os.getenv("ROOT_PATH", "/analytics")
app = FastAPI(
    title="Analytics Service",
    root_path=ROOT_PATH,
    docs_url=f"{ROOT_PATH}/docs" if ROOT_PATH else "/docs",
    redoc_url=f"{ROOT_PATH}/redoc" if ROOT_PATH else "/redoc",
    openapi_url=f"{ROOT_PATH}/openapi.json" if ROOT_PATH else "/openapi.json",
)
app.include_router(analytics_router)
