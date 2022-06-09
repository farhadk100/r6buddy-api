from fastapi import FastAPI, Security

from v1.endpoints import operators, weapons, gadgets
from v1.security import get_api_key

app = FastAPI(
    title="R6Buddy API",
    dependencies=[Security(get_api_key)]
)

app.include_router(operators.router)
app.include_router(weapons.router)
app.include_router(gadgets.router)


@app.get("/")
async def api_status():
    return {"status": "ok"}
