import pytest

from app.users.auth import verify_password
from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email,password,is_verify_password,is_present",
    [
        (1, "test@test.com", "admin", True, True),
        (1, "test@test.com", "add", False, True),
        (2, "test@test.com", "add", False, False),
    ],
)
async def test_find_user_by_id(
    user_id, email, password, is_verify_password, is_present
):
    user = await UsersDAO.find_by_id(user_id)

    if is_present:
        assert user.id == user_id
        assert user.email == email
        assert verify_password(password, user.hashed_password) is is_verify_password
