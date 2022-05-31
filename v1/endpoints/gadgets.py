from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.gadget import Gadget

router = APIRouter(
    prefix="/gadgets",
    tags=["gadgets"]
)


@router.get("/")
async def get_all_gadgets():
    return db["gadgets"].fetch()


@router.get("/{name}")
async def get_single_gadget(name: str):
    return db["gadgets"].get(name)


@router.put("/")
async def create_gadget(gadget: Gadget):
    return db["gadgets"].put(jsonable_encoder(gadget), key=gadget.name)


@router.delete("/{name}")
async def delete_gadget(name: str):
    return db["gadgets"].delete(name)
