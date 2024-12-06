from pydantic import BaseModel, Field
from typing import Annotated, Optional

Weight = Annotated[float, "Weight in gramms"]
BasketCapacity = Annotated[float, "Basket's capacity in gramms"]


class Mushroom(BaseModel):
    id: int
    name: str
    is_eatable: bool
    weight: Weight
    is_fresh: bool


class Basket(BaseModel):
    id: int
    owner: str
    capacity: BasketCapacity
    mushrooms: Optional[list[Mushroom]] = Field(default=[])


class BasketPut(BaseModel):
    basket_id: int
    mushroom_id: int
