import pytest_asyncio


@pytest_asyncio.fixture
async def client(aiohttp_client):
    from coldperson.app import make_app

    app = make_app()
    client = await aiohttp_client(app)
    return client
