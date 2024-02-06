from typing import Any, Generator

import aiohttp
from aiohttp import test_utils
import pytest
from pact import Consumer, Provider, Term
from pact.pact import Pact

from coldperson.knitter import Knitter, Sweater, SweaterOrder


def test_sweater_order_deserialization():
    from coldperson.knitter import SweaterOrder

    assert SweaterOrder.from_dict(
        {
            "colour": "white",
            "order_number": 1,
        }
    ) == SweaterOrder("white", 1)

    with pytest.raises(ValueError):
        SweaterOrder.from_dict(
            {
                "colour": None,
                "order_number": 1,
            }
        )


@pytest.fixture(scope="module")
def pact_server() -> Generator[Pact, Any, None]:
    pact = Consumer("ColdPerson").has_pact_with(
        Provider("Knitter"),
        pact_dir="pacts",
        host_name="localhost",
        port=test_utils.unused_port(),
    )

    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.fixture
def knitter_pact(pact_server: Pact, monkeypatch: pytest.MonkeyPatch) -> Pact:
    # Monkeypatching cannot go in the session scoped pact_server fixture
    monkeypatch.setenv("KNITTER_BASE_URL", pact_server.uri)
    return pact_server


@pytest.mark.asyncio
async def test_knitter__get_sweater(knitter_pact: Pact):
    # This is not actually the test that Holly writes
    # She writes a test that again tests the coldperson's endpoint
    # and uses the pact a mock

    expected = {
        "colour": "white",
        "order_number": 28,
    }

    (
        knitter_pact.upon_receiving("an order for a white sweater")
        .with_request(
            "POST",
            "/sweater/order",
            headers={"Content-Type": "application/json"},
            body={"colour": "white", "order_number": 28},
        )
        .will_respond_with(
            200,
            body=expected,
            headers={
                "Content-Type": Term("application/json(; .*)?", "application/json"),
            },
        )
    )

    with knitter_pact:
        async with aiohttp.ClientSession() as session:
            knitter = Knitter(session)
            result = await knitter.get_sweater(
                SweaterOrder(
                    colour="white",
                    order_number=28,
                )
            )

    assert result == Sweater(colour="white", order_number=28)
