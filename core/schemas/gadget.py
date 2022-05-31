from pydantic import BaseModel, Field


class Gadget(BaseModel):
    name: str = Field(description="unique gadget name")
    image_url: str
