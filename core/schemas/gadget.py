import strawberry
from pydantic import BaseModel, Field
from strawberry.scalars import ID


class Gadget(BaseModel):
    """ Schema for a gadget """
    name: str = Field(description="unique gadget name")
    image_url: str

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class GadgetOut(Gadget):
    """ Schema for a gadget that gets returned as output """
    key: str


@strawberry.type(name="Gadget")
class GadgetGQL:
    """ GraphQL schema for a gadget """
    key: ID
    name: str
    image_url: str


@strawberry.input(name="GadgetInput")
class GadgetInputGQL:
    """ GraphQL schema for a gadget that gets provided as input """
    name: str
    image_url: str
