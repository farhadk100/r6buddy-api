from pydantic import BaseModel, Field


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
