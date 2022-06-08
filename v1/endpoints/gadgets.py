from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.gadget import Gadget, GadgetOut
from core.utils import create_key

router = APIRouter(
    prefix="/gadgets",
    tags=["gadgets"]
)


@router.get("/", response_model=list[GadgetOut])
async def get_all_gadgets():
    gadgets = db["gadgets"].fetch().items
    return gadgets


@router.get("/{name}", response_model=GadgetOut)
async def get_single_gadget(name: str):
    gadget = db["gadgets"].get(create_key(name))
    if gadget is None:
        raise HTTPException(status_code=404, detail=f"Gadget with name '{name}' not found.")

    return gadget


@router.put("/", response_model=GadgetOut, status_code=201)
async def create_gadget(gadget: Gadget):
    gadget_db = db["gadgets"].put(jsonable_encoder(gadget), key=create_key(gadget.name))
    return gadget_db


@router.delete("/{name}")
async def delete_gadget(name: str):
    if db["gadgets"].get(create_key(name)) is None:
        raise HTTPException(status_code=404, detail=f"Gadget with name '{name}' not found.")

    db["gadgets"].delete(create_key(name))
    return {"status": "deleted"}
