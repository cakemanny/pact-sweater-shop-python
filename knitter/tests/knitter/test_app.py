from aiohttp import test_utils
import pytest
import pytest_asyncio
from pact import Consumer, Provider, Like, Term
from pact.pact import Pact


@pytest_asyncio.fixture
async def client(aiohttp_client):
    from knitter.app import make_app

    app = make_app()
    client = await aiohttp_client(app)
    return client


@pytest.fixture(scope="session")
def pact_server():
    pact = Consumer("Knitter").has_pact_with(
        Provider("Farmer"),
        pact_dir="pacts",
        host_name="localhost",
        port=test_utils.unused_port(),
    )
    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.fixture
def farmer_pact(pact_server, monkeypatch: pytest.MonkeyPatch):
    # Monkeypatching cannot go in the session scoped pact_server fixture
    monkeypatch.setenv(
        "FARMER_BASE_URL", f"http://{pact_server.host_name}:{pact_server.port}"
    )
    return pact_server


@pytest.mark.asyncio
async def test_healthz(client):
    resp = await client.get("/healthz")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_knit_sweater(client, farmer_pact: Pact):
    (
        farmer_pact.upon_receiving("an order for some wool")
        .with_request(
            "POST",
            "/wool/order",
            headers={"Content-Type": "application/json"},
            body=Like(
                {
                    "colour": "white",
                    "order_number": 12,
                }
            ),
        )
        .will_respond_with(
            200,
            headers={
                "Content-Type": Term("application/json(; .*)?", "application/json")
            },
            body=Like(
                {
                    "colour": "white",
                }
            ),
        )
    )

    with farmer_pact:
        resp = await client.post(
            "/sweater/order",
            json={
                "colour": "white",
                "order_number": 142,
            },
        )
        assert resp.status == 200
        assert await resp.json() == {
            "colour": "white",
            "order_number": 142,
            "style": "long_sleeved",
        }
