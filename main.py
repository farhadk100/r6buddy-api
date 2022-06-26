from fastapi import FastAPI, Security

from v1.endpoints import operators, weapons, gadgets, graphql
from v1.security import get_api_key

app = FastAPI(
    title="R6Buddy API"
)

app.include_router(operators.router, dependencies=[Security(get_api_key)])
app.include_router(weapons.router, dependencies=[Security(get_api_key)])
app.include_router(gadgets.router, dependencies=[Security(get_api_key)])
app.include_router(graphql.router)


@app.get("/")
async def api_status():
    return {"status": "ok"}
