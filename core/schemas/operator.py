import datetime
from pydantic import BaseModel


class Weapon(BaseModel):
    name: str
    image_url: str


class Gadget(BaseModel):
    name: str
    image_url: str


class OperatorLoadout(BaseModel):
    primary_weapons: set[str]
    secondary_weapons: set[str]
    gadgets: set[str]


class OperatorBio(BaseModel):
    real_name: str
    date_of_birth: datetime.date
    place_of_birth: str
    bio: str


class Operator(BaseModel):
    name: str
    speed: int
    armor: int
    icon_url: str
    bio: OperatorBio
    loadout: OperatorLoadout
