from fastapi import FastAPI
from v1.endpoints import operators, weapons, gadgets

app = FastAPI()

app.include_router(operators.router)
app.include_router(weapons.router)
app.include_router(gadgets.router)


@app.get("/")
async def api_status():
    return {"status": "ok"}
