import pytest
# import pytest_asyncio
from asgi_lifespan import LifespanManager

from httpx import AsyncClient

# from starlette.testclient import TestClient

from src.api.api import app
# from app.main import app


@pytest.fixture
async def async_test_client():
    # client = AsyncClient(app=app, base_url='http://localhost:8002')
    # return client

    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://localhost:8002',
                ) as client:
            yield client  # testing happens here

    # async with AsyncClient(
    #     app=app,
    #     base_url='http://localhost:8002'
    #         ) as client:
    #     yield client()  # testing happens here
