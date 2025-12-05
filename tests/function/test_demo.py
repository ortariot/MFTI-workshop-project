from http import HTTPStatus

from fastapi.testclient import TestClient
import pytest

from src.main import app
from src.models.category import Category


class TestDemo:

    @pytest.mark.asyncio
    async def test_misc(self, aiohttp_client):

        req_url = "/api/v1/misc/helth"

        response = await aiohttp_client.get(req_url)

        assert response.status == HTTPStatus.OK

        content = await response.json()

        assert content["status"] == "ok"
        # assert 3 == 1

    @pytest.mark.asyncio
    async def test_cat_all(self, aiohttp_client, test_session):

        req_url = "/api/v1/category/"

        category = Category(name="Электроника", desc="Гаджеты")

        test_session.add(category)
        await test_session.commit()

        response = await aiohttp_client.get(req_url)
        assert response.status == HTTPStatus.OK

        if response.status == HTTPStatus.OK:
            content = await response.json()

            assert len(content) == 1

    @pytest.mark.parametrize(
        "query_data, expected_data",
        [
            ({"limit": 1, "skip": 1, "addon": 10}, {"status": HTTPStatus.OK, "len": 1}),
            ({"limit": 10, "skip": 4, "addon": 0}, {"status": HTTPStatus.OK, "len": 6}),
            ({"limit": 30, "skip": 40, "addon": 10}, {"status": HTTPStatus.NOT_FOUND, "len": 1}),
        ],
    )
    @pytest.mark.asyncio
    async def test_cat_all_param(
        self, query_data, expected_data, aiohttp_client, test_session
    ):

        req_url = f"/api/v1/category/?limit={query_data['limit']}&skip={query_data['skip']}"


        for i in range(query_data['limit'] + query_data['addon']):

            category = Category(name=f"Электроника-{i}", desc=f"Гаджеты-{i}")
            test_session.add(category)

        await test_session.commit()

        response = await aiohttp_client.get(req_url)

        assert response.status == expected_data["status"]

        if response.status == expected_data["status"]:
            content = await response.json()

            assert len(content) == expected_data["len"]
