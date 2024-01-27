from enum import Enum
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Farmer",
    version="0.1.0",
)


class Order(BaseModel):
    colour: str
    order_number: int


class Sheep(str, Enum):
    white = "white"
    black = "black"
    grey = "grey"
    brown = "brown"

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


@app.post(
    "/wool/order",
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "white": {
                            "value": {
                                "colour": "white",
                                "order_number": 28,
                                "weight": "worsted",
                            }
                        },
                        "black": {
                            "value": {
                                "colour": "black",
                                "order_number": 97,
                                "weight": "chunky",
                            }
                        },
                    }
                }
            }
        }
    },
    openapi_extra={
        "x-microcks-operation": {
            "dispatcher": "JSON_BODY",
            "dispatcherRules": {
                "exp": "/colour",
                "operator": "equals",
                "cases": {
                    "black": "black",
                    "default": "white"
                }
            }
        }
    },
)
async def shear_sheep(
    order: Annotated[
        Order,
        Body(
            openapi_examples={
                "white": {
                    "value": Order(
                        colour="white",
                        order_number=28,
                    ).model_dump()
                },
                "black": {
                    "value": Order(
                        colour="black",
                        order_number=97,
                    ).model_dump()
                },
            }
        ),
    ]
) -> Skein:
    sheep: Sheep
    try:
        sheep = getattr(Sheep, order.colour.lower())
    except AttributeError:
        sheep = Sheep.white
    return Skein.from_sheep(sheep, order.order_number)


@app.get("/healthz")
async def healthz() -> str:
    return "Alles jut!"
