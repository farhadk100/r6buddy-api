from typing import Union

import strawberry
from strawberry.fastapi import GraphQLRouter

from core.models.database import db
from core.schemas.gadget import GadgetGQL
from core.schemas.operator import OperatorGQL, OperatorType, OperatorLoadoutGQL
from core.schemas.weapon import WeaponGQL
from core.utils import create_key
from v1.endpoints.operators import get_weapons, get_gadgets


@strawberry.type
class Query:
    @strawberry.field
    def weapon(self, name: str) -> WeaponGQL:
        weapon = db["weapons"].get(create_key(name))
        if weapon is None:
            raise Exception(f"Weapon with name '{name}' not found.")
        return WeaponGQL(**weapon)

    @strawberry.field
    def weapons(self) -> list[WeaponGQL]:
        weapons = db["weapons"].fetch().items
        return [WeaponGQL(**weapon) for weapon in weapons]

    @strawberry.field
    def gadget(self, name: str) -> GadgetGQL:
        gadget = db["gadgets"].get(create_key(name))
        if gadget is None:
            raise Exception(f"Gadget with name '{name}' not found.")
        return GadgetGQL(**gadget)

    @strawberry.field
    def gadgets(self) -> list[GadgetGQL]:
        gadgets = db["gadgets"].fetch().items
        return [GadgetGQL(**gadget) for gadget in gadgets]

    @strawberry.field
    def operator(self, name: str) -> OperatorGQL:
        operator = db["operators"].get(create_key(name))
        if operator is None:
            raise Exception(f"Operator with name '{name}' not found.")
        return OperatorGQL(**operator)

    @strawberry.field
    def operators(self, type: Union[OperatorType, None] = None) -> list[OperatorGQL]:
        if type:
            db_operators = db["operators"].fetch(query={"type": type}).items
        else:
            db_operators = db["operators"].fetch().items

        # get all weapons and gadgets
        weapons_dict = get_weapons()
        gadgets_dict = get_gadgets()

        try:
            operators = []
            for db_op in db_operators:
                # for each operator, create their loadout
                primary_weapons = [WeaponGQL(**weapons_dict[create_key(w_id)]) for w_id in
                                   db_op["loadout"]["primary_weapons"]]
                secondary_weapons = [WeaponGQL(**weapons_dict[create_key(w_id)]) for w_id in
                                     db_op["loadout"]["secondary_weapons"]]
                gadgets = [gadgets_dict[create_key(g_id)] for g_id in db_op["loadout"]["gadgets"]]

                # create a new OperatorOut object
                operator = OperatorGQL(
                    key=db_op["key"],
                    name=db_op["name"],
                    type=db_op["type"],
                    speed=db_op["speed"],
                    armor=db_op["armor"],
                    icon_url=db_op["icon_url"],
                    portrait_url=db_op["portrait_url"],
                    bio=db_op["bio"],
                    loadout=OperatorLoadoutGQL(
                        primary_weapons=primary_weapons,
                        secondary_weapons=secondary_weapons,
                        gadgets=gadgets
                    )
                )
                operators.append(operator)
            return operators
        except KeyError:
            raise Exception("One or more weapons and/or gadgets not found.")


schema = strawberry.Schema(query=Query)

router = GraphQLRouter(schema=schema, path="/graphql")
