from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.weapon import Weapon, WeaponOut
from core.utils import create_key

router = APIRouter(
    prefix="/weapons",
    tags=["weapons"]
)


@router.get("/", response_model=list[WeaponOut])
async def get_all_weapons():
    weapons = db["weapons"].fetch().items
    return weapons


@router.get("/{name}", response_model=WeaponOut)
async def get_single_weapon(name: str):
    weapon = db["weapons"].get(create_key(name))
    if weapon is None:
        raise HTTPException(status_code=404, detail=f"Weapon with name '{name}' not found.")

    return weapon


@router.put("/", response_model=WeaponOut, status_code=201)
async def create_weapon(weapon: Weapon):
    weapon_db = db["weapons"].put(jsonable_encoder(weapon), key=create_key(weapon.name))
    return weapon_db


@router.delete("/{name}")
async def delete_weapon(name: str):
    if db["weapons"].get(create_key(name)) is None:
        raise HTTPException(status_code=404, detail=f"Weapon with name '{name}' not found.")

    db["weapons"].delete(create_key(name))
    return {"status": "deleted"}
