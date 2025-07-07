from fastapi import FastAPI
import os
from .api import router as analytics_router

app = FastAPI(title="Analytics Service", root_path=os.getenv("ROOT_PATH", ""))
app.include_router(analytics_router)
