import base64
from typing import Any, Generator

import pytest
from aiohttp import test_utils
from pact import Consumer, Provider, Term
from pact.pact import Pact


@pytest.fixture(scope="module")
def pact_server() -> Generator[Pact, Any, None]:
    pact = Consumer("ColdPerson").has_pact_with(
        Provider("Hatter"),
        pact_dir="pacts",
        host_name="localhost",
        port=test_utils.unused_port(),
    )

    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.fixture
def hatter_pact(pact_server: Pact, monkeypatch: pytest.MonkeyPatch) -> Pact:
    # Monkeypatching cannot go in the session scoped pact_server fixture
    monkeypatch.setenv("HATTER_BASE_URL", pact_server.uri)
    return pact_server


@pytest.fixture
def hatter_auth_header():
    # Load from a secret store
    encoded = base64.urlsafe_b64encode(b"cold-person:im-a-freezin").decode()
    return f"Basic {encoded}"


@pytest.mark.asyncio
async def test_ordering_hat(hatter_pact: Pact, client, hatter_auth_header):
    (
        hatter_pact.given("cold-person has an account with the hatter")
        .upon_receiving("an order for a wooly hat")
        .with_request(
            "POST",
            "/hat/order",
            headers={
                "Content-Type": "application/json",
                "Authorization": hatter_auth_header,
            },
            body={
                "colour": "green",
                "order_number": 27,
                "material": "wool",
            },
        )
        .will_respond_with(
            200,
            body={
                "colour": "green",
                "order_number": 27,
                "material": "wool",
            },
            headers={
                "Content-Type": Term("application/json(; .*)?", "application/json"),
            },
        )
    )

    with hatter_pact:
        resp = await client.post(
            "/bff/order/hat",
            json={"colour": "green", "order_number": 27, "material": "wool"},
        )

    assert resp.status == 200
    assert await resp.json() == {
        "colour": "green",
        "order_number": 27,
        "material": "wool",
    }
