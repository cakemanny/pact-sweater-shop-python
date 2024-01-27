from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Order(BaseModel):
    colour: str
    order_number: int


class Sheep(str, Enum):
    white = "white"
    black = "black"
    grey = 'grey'
    brown = 'brown'

    def __str__(self) -> str:
        return str.__str__(self)


class Weight(str, Enum):
    WORSTED = "worsted"
    CHUNKY = "chunky"

    def __str__(self) -> str:
        return str.__str__(self)


class Skein(BaseModel):
    colour: str
    order_number: int
    weight: Weight = Weight.WORSTED

    @classmethod
    def from_sheep(cls, sheep: Sheep, order_number: int):
        """
        Given a sheep, get usable wool from the sheep
        """
        return cls(colour=sheep.name, order_number=order_number)


@app.post("/wool/order")
async def shear_sheep(order: Order) -> Skein:
    sheep: Sheep
    try:
        sheep = getattr(Sheep, order.colour.lower())
    except AttributeError:
        sheep = Sheep.white
    return Skein.from_sheep(sheep, order.order_number)


@app.get("/healthz")
async def healthz() -> str:
    return 'Alles jut!'
