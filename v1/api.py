from fastapi import FastAPI
from .endpoints import operators, weapons, gadgets

api = FastAPI()

api.include_router(operators.router)
api.include_router(weapons.router)
api.include_router(gadgets.router)


@api.get("/status")
async def api_status():
    return {"status": "ok"}
