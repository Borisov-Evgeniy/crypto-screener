import pytest
from backend.app.models.user import User
from backend.app.repositories.user_repositories import InvalidPasswordError,UserNotFoundError

@pytest.mark.asyncio
async def test_create_and_get_user(user_repository):
    user = await user_repository.create_user("test@example.com", "hashedpass")
    fetched = await user_repository.get_user_by_id(user.id)
    assert fetched.email == "test@example.com"
    assert fetched.hashed_password == "hashedpass"

@pytest.mark.asyncio
async def test_get_user_by_id(user_repository):
    created = await user_repository.create_user("byid@example.com", "123")
    user = await user_repository.get_user_by_id(created.id)
    assert user is not None
    assert user.id == created.id

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repository):
    user = await user_repository.get_user_by_id(9999)
    assert user is None

@pytest.mark.asyncio
async def test_update_user_email(user_repository):
    user = await user_repository.create_user("old@example.com", "hashedpass")
    updated = await user_repository.update_user_email(user.id, "new@example.com")
    assert updated.email == "new@example.com"

@pytest.mark.asyncio
async def test_duplicate_email(user_repository):
    await user_repository.create_user("dupe@example.com", "pass")
    with pytest.raises(Exception):
        await user_repository.create_user("dupe@example.com", "other")

@pytest.mark.asyncio
async def test_get_user_by_email_not_found(user_repository):
    user = await user_repository.get_user_by_email("missing@example.com")
    assert user is None

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