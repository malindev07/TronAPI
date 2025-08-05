import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_check_bandwidth_energy_balance_valid_addr(client: AsyncClient) -> None:
    response = await client.post(
        "/wallet/resources",
        params={"address": "TQAXVqxCHPGEAQMn945kta22FUicd28SLo"},  # valid addr
    )
    assert "balance" in response.json()
    assert "bandwidth" in response.json()
    assert "energy" in response.json()
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_check_bandwidth_energy_balance_invalid_addr(client: AsyncClient) -> None:
    response = await client.post(
        "/wallet/resources",
        params={"address": "TQAXVqxCHPGEAQMn925kta22FUicd28SLo"},  # invalid addr
    )
    assert "balance" not in response.json()
    assert "bandwidth" not in response.json()
    assert "energy" not in response.json()
    assert response.json()["msg"] == "Not found"
    assert response.status_code == 404
