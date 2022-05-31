from fastapi import FastAPI
from .endpoints import operators

api = FastAPI()

api.include_router(operators.router)


@api.get("/status")
async def api_status():
    return {"status": "ok"}
