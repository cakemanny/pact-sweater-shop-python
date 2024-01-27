import pytest
import aiohttp
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from knitter.farmer import Farmer, WoolOrder


# See https://github.com/testcontainers/testcontainers-python for
# examples of how these are written and
# https://github.com/microcks/microcks-testcontainers-java
# for details related to microcks
class MicrocksContainer(DockerContainer):
    def __init__(self, image="quay.io/microcks/microcks-uber:1.8.1", **kwargs):
        super().__init__(image, **kwargs)

        self.http_port = 8080
        self.grpc_port = 9090
        self.with_exposed_ports(self.http_port, self.grpc_port)

    def start(self) -> "MicrocksContainer":
        super().start()
        wait_for_logs(self, ".*Started MicrocksApplication.*")
        return self

    def get_http_endpoint(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.http_port)
        return f"http://{host}:{port}"

    # skipping get_soap_mock_endpoint
    def get_rest_mock_endpoint(self, service: str, version: str) -> str:
        return f"{self.get_http_endpoint()}/rest/{service}/{version}"

    # skipping graphql and grpc

    async def import_as_main_artifact(self, path: str):
        await self._import_artifact(path)

    async def import_as_secondary_artifact(self, path: str):
        await self._import_artifact(path, is_main=False)

    async def test_endpoint(self, test_request):
        raise NotImplementedError

    # If we didn't already have aiohttp, I'd think to use urllib
    async def _import_artifact(self, path: str, is_main: bool = True):
        async with aiohttp.ClientSession() as session:
            with open(path, "rb") as f:
                params = {"mainArtifact": str(is_main).lower()}
                files = {"file": f}
                endpoint = self.get_http_endpoint() + "/api/artifact/upload"
                async with session.post(endpoint, params=params, data=files) as resp:
                    if resp.status != 201:
                        raise Exception(
                            "Artifact has not been correctly been imported:",
                            resp.text(),
                        )


@pytest.fixture(scope="module")
def microcks():
    with MicrocksContainer() as container:
        yield container


@pytest.mark.skip("experimental")
@pytest.mark.asyncio
async def test_farmer_client(microcks, monkeypatch):
    await microcks.import_as_main_artifact("specs/Farmer-openapi.json")

    base_url = microcks.get_rest_mock_endpoint("Farmer", "0.1.0")
    monkeypatch.setenv("FARMER_BASE_URL", base_url)

    async with aiohttp.ClientSession() as session:
        farmer_client = Farmer(session)

        skein = await farmer_client.get_wool(WoolOrder("white", 28))

        assert skein.colour == 'white'
