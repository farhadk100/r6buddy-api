from pydantic import BaseModel, Field


class Weapon(BaseModel):
    name: str = Field(description="unique weapon name")
    image_url: str
