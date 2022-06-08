import datetime
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl

from core.schemas.gadget import GadgetOut
from core.schemas.weapon import WeaponOut


class OperatorType(str, Enum):
    attacker = "attacker"
    defender = "defender"


class OperatorBio(BaseModel):
    real_name: str
    date_of_birth: datetime.date
    place_of_birth: str
    bio: str


class OperatorBase(BaseModel):
    """ Base class for all operator schemas """
    name: str
    type: OperatorType = Field(description="'attacker' or 'defender'")
    speed: int
    armor: int
    icon_url: HttpUrl = Field(description="url to an image of operators' icon")
    portrait_url: HttpUrl = Field(description="url to an image of operators' portrait")
    bio: OperatorBio


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
