from pydantic import BaseModel, Field


class Weapon(BaseModel):
    """ Schema for a weapon """
    name: str = Field(description="unique weapon name")
    image_url: str


class WeaponOut(Weapon):
    """ Schema for a weapon that gets returned as output """
    key: str
