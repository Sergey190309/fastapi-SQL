import pytest
from httpx import AsyncClient
# from src.api.api import app

# pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
# @pytest.mark.active
async def test_ping(async_test_client: AsyncClient):
    response = await async_test_client.get('/ping/')
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
