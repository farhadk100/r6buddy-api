from enum import Enum

import strawberry
from pydantic import BaseModel, Field, HttpUrl
from strawberry.scalars import ID

from core.schemas.gadget import GadgetOut, GadgetGQL, GadgetInputGQL
from core.schemas.weapon import WeaponOut, WeaponGQL, WeaponInputGQL


@strawberry.enum()
class OperatorType(str, Enum):
    attacker = "Attacker"
    defender = "Defender"


class OperatorBio(BaseModel):
    real_name: str
    date_of_birth: str
    place_of_birth: str
    biography: str
    psychological_report: str


class OperatorAbility(BaseModel):
    name: str
    image_url: HttpUrl
    playstyle: str


class OperatorBase(BaseModel):
    """ Base class for all operator schemas """
    name: str
    type: OperatorType = Field(description="'Attacker' or 'Defender'")
    speed: int
    armor: int
    icon_url: HttpUrl = Field(description="url to an image of operators' icon")
    portrait_url: HttpUrl = Field(description="url to an image of operators' portrait")
    bio: OperatorBio
    unique_ability: OperatorAbility

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class OperatorLoadoutIn(BaseModel):
    """ Schema for the loadout of an operator that gets provided as input """
    primary_weapons: list[str] = Field(description="list of names (keys) of existing primary weapons")
    secondary_weapons: list[str] = Field(description="list of names (keys) of existing secondary weapons")
    gadgets: list[str] = Field(description="list of names of gadgets")


class OperatorLoadoutOut(BaseModel):
    """ Schema for the loadout of an operator that gets returned as output """
    primary_weapons: list[WeaponOut] = Field(description="list of primary weapons")
    secondary_weapons: list[WeaponOut] = Field(description="list of secondary weapons")
    gadgets: list[GadgetOut] = Field(description="list of gadgets")


class OperatorIn(OperatorBase):
    """ Schema for an operator that gets provided as input """
    loadout: OperatorLoadoutIn


class OperatorOut(OperatorBase):
    """ Schema for an operator that gets returned as output """
    key: str
    loadout: OperatorLoadoutOut


@strawberry.type(name="OperatorBio")
class OperatorBioGQL:
    """ GraphQL schema for an operator's bio """
    real_name: str
    date_of_birth: str
    place_of_birth: str
    bio: str


@strawberry.type(name="OperatorLoadout")
class OperatorLoadoutGQL:
    """ GraphQL schema for an operator's loadout """
    primary_weapons: list[WeaponGQL]
    secondary_weapons: list[WeaponGQL]
    gadgets: list[GadgetGQL]


@strawberry.type(name="Operator")
class OperatorGQL:
    """ GraphQL schema for an operator """
    key: ID
    name: str
    type: 'OperatorType'
    speed: int
    armor: int
    icon_url: str
    portrait_url: str
    bio: 'OperatorBioGQL'
    loadout: 'OperatorLoadoutGQL'


@strawberry.input(name="OperatorLoadoutInput")
class OperatorLoadoutInputGQL:
    """ GraphQL schema for an operator's loadout that gets provided as input """
    primary_weapons: list[WeaponInputGQL]
    secondary_weapons: list[WeaponInputGQL]
    gadgets: list[GadgetInputGQL]


@strawberry.type(name="Operator")
class OperatorInputGQL:
    """ GraphQL schema for an operator """
    name: str
    type: 'OperatorType'
    speed: int
    armor: int
    icon_url: str
    portrait_url: str
    bio: 'OperatorBioGQL'
    loadout: 'OperatorLoadoutInputGQL'
