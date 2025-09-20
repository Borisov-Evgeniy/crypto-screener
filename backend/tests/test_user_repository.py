import pytest
from backend.app.models.user import User

@pytest.mark.asyncio
async def test_create_and_get_user(user_repository):
    user = await user_repository.create_user("test@example.com", "hashedpass")
    fetched = await user_repository.get_user_by_id(user.id)
    assert fetched.email == "test@example.com"
    assert fetched.hashed_password == "hashedpass"


@pytest.mark.asyncio
async def test_update_user_email(user_repository):
    user = await user_repository.create_user("old@example.com", "hashedpass")
    updated = await user_repository.update_user_email(user.id, "new@example.com")
    assert updated.email == "new@example.com"


@pytest.mark.asyncio
async def test_change_user_status(user_repository):
    user = await user_repository.create_user("status@example.com", "hashedpass")
    updated = await user_repository.change_user_status(user.id, False)
    assert updated.is_active is False


@pytest.mark.asyncio
async def test_delete_user(user_repository):
    user = await user_repository.create_user("delete@example.com", "hashedpass")
    await user_repository.delete_user(user.id)
    deleted = await user_repository.get_user_by_id(user.id)
    assert deleted is None
