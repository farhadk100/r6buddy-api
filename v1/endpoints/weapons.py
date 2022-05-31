from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.weapon import Weapon

router = APIRouter(
    prefix="/weapons",
    tags=["weapons"]
)


@router.get("/")
async def get_all_weapons():
    return db["weapons"].fetch()


@router.get("/{name}")
async def get_single_weapon(name: str):
    return db["weapons"].get(name)


@router.put("/")
async def create_weapon(weapon: Weapon):
    return db["weapons"].put(jsonable_encoder(weapon), key=weapon.name)


@router.delete("/{name}")
async def delete_weapon(name: str):
    return db["weapons"].delete(name)
