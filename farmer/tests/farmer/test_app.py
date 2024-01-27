import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from farmer import app
    return TestClient(app)


@pytest.mark.parametrize("colour,order_number", [
    ("white", 2,),
    ("black", 4,),
])
def test_wool_endpoint(client: TestClient, colour, order_number):

    from farmer import Order, Skein
    order = Order(colour=colour, order_number=order_number)

    response = client.post(
        "/wool/order",
        json=order.model_dump(),
    )
    assert response.status_code == 200
    skein = Skein.model_validate(response.json())
    assert skein.colour == colour
