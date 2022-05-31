from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.operator import Operator

router = APIRouter(
    prefix="/operators",
    tags=["operators"]
)


@router.get("/")
async def get_all_operators():
    return db["operators"].fetch()


@router.post("/")
async def create_operator(operator: Operator):
    return db["operators"].put(jsonable_encoder(operator), key=operator.name)


@router.delete("/{name}")
async def delete_operator(name: str):
    return db["operators"].delete(name)
