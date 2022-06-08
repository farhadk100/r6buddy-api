from pydantic import BaseModel, Field


class Gadget(BaseModel):
    """ Schema for a gadget """
    name: str = Field(description="unique gadget name")
    image_url: str


class GadgetOut(Gadget):
    """ Schema for a gadget that gets returned as output """
    key: str
