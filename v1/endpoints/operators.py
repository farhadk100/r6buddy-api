from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from core.models.database import db
from core.schemas.gadget import Gadget
from core.schemas.operator import OperatorOut, OperatorLoadoutOut, OperatorIn, OperatorType
from core.schemas.weapon import Weapon
from core.utils import create_key

router = APIRouter(
    prefix="/operators",
    tags=["operators"]
)


def get_weapons() -> dict[str, Weapon]:
    """ helper function that gets all weapons from the database and puts them into a dict with key="key" """
    weapons = db["weapons"].fetch().items
    weapons_dict = {w["key"]: w for w in weapons}
    return weapons_dict


def get_gadgets() -> dict[str, Gadget]:
    """ helper function that gets all gadgets from the database and puts them into a dict with key="key" """
    gadgets = db["gadgets"].fetch().items
    gadgets_dict = {g["key"]: g for g in gadgets}
    return gadgets_dict


@router.get("/", response_model=list[OperatorOut])
async def get_all_operators(type: Union[OperatorType, None] = None):
    # get all operators
    if type:
        db_operators = db["operators"].fetch(query={"type": type})
    else:
        db_operators = db["operators"].fetch()

    # get all weapons and gadgets
    weapons_dict = get_weapons()
    gadgets_dict = get_gadgets()

    try:
        operators = []
        for db_op in db_operators.items:
            # for each operator, create their loadout
            primary_weapons = [weapons_dict[create_key(w_id)] for w_id in db_op["loadout"]["primary_weapons"]]
            secondary_weapons = [weapons_dict[create_key(w_id)] for w_id in db_op["loadout"]["secondary_weapons"]]
            gadgets = [gadgets_dict[create_key(g_id)] for g_id in db_op["loadout"]["gadgets"]]

            # create a new OperatorOut object
            operator = OperatorOut(
                key=db_op["key"],
                name=db_op["name"],
                type=db_op["type"],
                speed=db_op["speed"],
                armor=db_op["armor"],
                icon_url=db_op["icon_url"],
                portrait_url=db_op["portrait_url"],
                bio=db_op["bio"],
                loadout=OperatorLoadoutOut(
                    primary_weapons=primary_weapons,
                    secondary_weapons=secondary_weapons,
                    gadgets=gadgets
                )
            )
            operators.append(operator)
        return operators
    except KeyError:
        raise HTTPException(status_code=400, detail="One or more weapons and/or gadgets not found.")


@router.get("/{name}", response_model=OperatorOut)
async def get_single_operator(name: str):
    # get the operator
    db_op = db["operators"].get(create_key(name))
    if db_op is None:
        raise HTTPException(status_code=404, detail=f"Operator with name '{name}' not found")

    # get all weapons and gadgets for the operator
    weapons = get_weapons()
    gadgets = get_gadgets()

    try:
        primary_weapons = [weapons[create_key(w_id)] for w_id in db_op["loadout"]["primary_weapons"]]
        secondary_weapons = [weapons[create_key(w_id)] for w_id in db_op["loadout"]["secondary_weapons"]]
        gadgets = [gadgets[create_key(g_id)] for g_id in db_op["loadout"]["gadgets"]]

        # create a new OperatorOut object
        operator = OperatorOut(
            key=db_op["key"],
            name=db_op["name"],
            type=db_op["type"],
            speed=db_op["speed"],
            armor=db_op["armor"],
            icon_url=db_op["icon_url"],
            portrait_url=db_op["portrait_url"],
            bio=db_op["bio"],
            loadout=OperatorLoadoutOut(
                primary_weapons=primary_weapons,
                secondary_weapons=secondary_weapons,
                gadgets=gadgets
            )
        )
        return operator
    except KeyError:
        raise HTTPException(status_code=400, detail="One or more weapons and/or gadgets not found.")


@router.put("/", response_model=OperatorOut, status_code=201)
async def create_operator(operator: OperatorIn):
    weapons = get_weapons()
    gadgets = get_gadgets()

    # check that all operator weapons and gadgets exist in the db
    for w_id in operator.loadout.primary_weapons + operator.loadout.secondary_weapons:
        if create_key(w_id) not in weapons.keys():
            raise HTTPException(status_code=400, detail=f"Weapon with id '{w_id}' not found.")

    for g_id in operator.loadout.gadgets:
        if create_key(g_id) not in gadgets.keys():
            raise HTTPException(status_code=400, detail=f"Gadget with id '{g_id}' not found.")

    # insert the operator in the database and return it
    operator_db = db["operators"].put(jsonable_encoder(operator), key=create_key(operator.name))

    return OperatorOut(
        key=operator_db["key"],
        name=operator_db["name"],
        type=operator_db["type"],
        speed=operator_db["speed"],
        armor=operator_db["armor"],
        icon_url=operator_db["icon_url"],
        portrait_url=operator_db["portrait_url"],
        bio=operator_db["bio"],
        loadout=OperatorLoadoutOut(
            primary_weapons=[weapons[create_key(w_id)] for w_id in operator_db["loadout"]["primary_weapons"]],
            secondary_weapons=[weapons[create_key(w_id)] for w_id in operator_db["loadout"]["secondary_weapons"]],
            gadgets=[gadgets[create_key(g_id)] for g_id in operator_db["loadout"]["gadgets"]]
        )
    )


@router.delete("/{name}")
async def delete_operator(name: str):
    if db["operators"].get(create_key(name)) is None:
        raise HTTPException(status_code=404, detail=f"Operator with name '{name}' not found.")

    db["operators"].delete(create_key(name))
    return {"status": "deleted"}
