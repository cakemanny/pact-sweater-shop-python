from typing import Any, Generator

import aiohttp
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


@pytest.fixture(scope="session")
def pact() -> Generator[Pact, Any, None]:
    pact = Consumer("ColdPerson").has_pact_with(
        Provider("Knitter"),
        pact_dir="pacts",
        host_name="localhost",
        # Port 1234 is the default port of PACT
        # aiohttp.test_utils has an unused_port function if this breaks
        port=1234,
    )

    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.mark.asyncio
async def test_knitter__get_sweater(pact, monkeypatch: pytest.MonkeyPatch):
    # This is not actually the test that Holly writes
    # She writes a test that again tests the coldperson's endpoint
    # and uses the pact a mock

    monkeypatch.setenv("KNITTER_BASE_URL", f"http://{pact.host_name}:{pact.port}")

    expected = {
        "colour": "white",
        "order_number": 28,
    }

    (
        pact.upon_receiving("an order for a white sweater")
        .with_request(
            "POST",
            "/sweater/order",
            body={"colour": "white", "order_number": 28},
            headers={"Content-Type": "application/json"},
        )
        .will_respond_with(
            200,
            body=expected,
            headers={
                "Content-Type": Term("application/json(; .*)?", "application/json"),
            }
        )
    )

    with pact:
        async with aiohttp.ClientSession() as session:
            knitter = Knitter(session)
            result = await knitter.get_sweater(
                SweaterOrder(
                    colour="white",
                    order_number=28,
                )
            )

    assert result == Sweater(colour="white", order_number=28)
