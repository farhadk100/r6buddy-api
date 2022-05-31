import datetime
from pydantic import BaseModel, Field


class OperatorLoadout(BaseModel):
    primary_weapons: set[str] = Field(description="set of names (keys) of primary weapons")
    secondary_weapons: set[str] = Field(description="set of names (keys) of secondary weapons")
    gadgets: set[str] = Field(description="set of names of gadgets")


class OperatorBio(BaseModel):
    real_name: str
    date_of_birth: datetime.date
    place_of_birth: str
    bio: str


class Operator(BaseModel):
    name: str
    speed: int
    armor: int
    icon_url: str = Field(description="url to an image of operators' icon")
    bio: OperatorBio
    loadout: OperatorLoadout
