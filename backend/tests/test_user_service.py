import pytest
from backend.app.core.security import password_hasher

@pytest.mark.asyncio
async def test_create_user_and_authenticate(user_service):
    user = await user_service.create_user("auth@example.com", "mypassword")
    assert user.hashed_password != "mypassword"  # пароль захеширован

    auth_user = await user_service.authenticate_user("auth@example.com", "mypassword")
    assert auth_user is not None
    assert auth_user.email == "auth@example.com"

@pytest.mark.asyncio
async def test_change_password(user_service):
    user = await user_service.create_user("changepass@example.com", "oldpass")
    updated = await user_service.change_password(user.id, "newpass")
    assert password_hasher.verify_password("newpass", updated.hashed_password)

@pytest.mark.asyncio
async def test_change_email(user_service):
    user = await user_service.create_user("oldmail@example.com", "pass")
    updated = await user_service.change_email(user.id, "newmail@example.com")
    assert updated.email == "newmail@example.com"

@pytest.mark.asyncio
async def test_change_status(user_service):
    user = await user_service.create_user("status@example.com", "pass")
    updated = await user_service.change_status(user.id, False)
    assert updated.is_active is False

@pytest.mark.asyncio
async def test_delete_user(user_service):
    user = await user_service.create_user("delete@example.com", "pass")
    await user_service.delete_user(user.id)
    deleted = await user_service.user_repository.get_user_by_id(user.id)
    assert deleted is None
