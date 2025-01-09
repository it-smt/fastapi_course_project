import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("test@test.com", "admin", 409),
        ("abcd", "admin", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    resp = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "admin", 200),
        ("artem@example.com", "admin", 200),
        ("asas@example.com", "admin", 401),
        ("asas", "admin", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    resp = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert resp.status_code == status_code
