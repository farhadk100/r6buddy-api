from enum import Enum
from typing import Union

import strawberry
from pydantic import BaseModel, Field
from strawberry.scalars import ID


@strawberry.enum(name='WeaponType')
class WeaponType(str, Enum):
    """ Enum for the type of a weapon """
    assault_rifle = 'Assault Rifle',
    shotgun = 'Shotgun',
    handgun = 'Handgun',
    submachine_gun = 'Submachine Gun',
    light_machine_gun = 'Light Machine Gun',
    hand_cannon = 'Hand Cannon',
    machine_pistol = 'Machine Pistol',
    marksman_rifle = 'Marksman Rifle'


class Weapon(BaseModel):
    """ Schema for a weapon """
    name: str = Field(description="unique weapon name")
    image_url: str
    type: Union[WeaponType, None] = Field(
        description="type of weapon. Can be nullable for some occasions (e.g. Blitz's shield)")

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class WeaponOut(Weapon):
    """ Schema for a weapon that gets returned as output """
    key: str


@strawberry.type(name="Weapon")
class WeaponGQL:
    """ GraphQL schema for a weapon"""
    key: ID
    name: str
    image_url: str
    type: Union['WeaponType', None]


@strawberry.input(name="WeaponInput")
class WeaponInputGQL:
    """ GraphQL schema for a weapon that gets provided as input """
    name: str
    image_url: str
    type: Union['WeaponType', None]
