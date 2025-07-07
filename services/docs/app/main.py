import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
import httpx

SERVICES = {
    "auth": {"url": "http://auth:8000/openapi.json", "prefix": "/auth"},
    "profile": {"url": "http://profile:8000/openapi.json", "prefix": "/profile"},
    "content": {"url": "http://content:8000/docs/swagger.json", "prefix": "/content"},
    "chat": {"url": "http://chat:3000/swagger.json", "prefix": "/chat"},
    "notification": {"url": "http://notification:8000/openapi.json", "prefix": "/notification"},
    "analytics": {"url": "http://analytics:8000/openapi.json", "prefix": "/analytics"},
}

app = FastAPI(title="Combined API", docs_url=None, openapi_url=None)

async def build_openapi():
    paths = {}
    components = {}
    async with httpx.AsyncClient() as client:
        for name, cfg in SERVICES.items():
            try:
                resp = await client.get(cfg["url"])
                resp.raise_for_status()
                spec = resp.json()
            except Exception:
                continue
            prefix = cfg["prefix"]
            for path, path_item in spec.get("paths", {}).items():
                paths[prefix + path] = path_item
            for comp_type, comps in spec.get("components", {}).items():
                components.setdefault(comp_type, {})
                for comp_name, comp_schema in comps.items():
                    components[comp_type][f"{name}_{comp_name}"] = comp_schema
    return {
        "openapi": "3.0.0",
        "info": {"title": "evapps Combined API", "version": "1.0"},
        "paths": paths,
        "components": components,
    }

@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    spec = await build_openapi()
    return JSONResponse(spec)

@app.get("/docs", include_in_schema=False)
async def docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Combined API")
