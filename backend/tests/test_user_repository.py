import pytest
from backend.repositories.user_repositories import InvalidPasswordError

# тесты используют фикстуру user_repo из conftest.py

@pytest.mark.asyncio
async def test_create_user(user_repo):
    user = await user_repo.create_user("test@example.com", "password123")
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.hashed_password != "password123"

@pytest.mark.asyncio
async def test_get_user_by_email(user_repo):
    await user_repo.create_user("findme@example.com", "123")
    user = await user_repo.get_user_by_email("findme@example.com")
    assert user is not None
    assert user.email == "findme@example.com"

@pytest.mark.asyncio
async def test_verify_password_user_correct(user_repo):
    await user_repo.create_user("auth@example.com", "secret")
    result = await user_repo.verify_password_user("auth@example.com", "secret")
    assert result is True

@pytest.mark.asyncio
async def test_verify_password_user_invalid(user_repo):
    await user_repo.create_user("auth2@example.com", "secret")
    with pytest.raises(InvalidPasswordError):
        await user_repo.verify_password_user("auth2@example.com", "wrong")

@pytest.mark.asyncio
async def test_update_user_email(user_repo):
    user = await user_repo.create_user("old@example.com", "pass")
    updated = await user_repo.update_user_email(user.id, "new@example.com")
    assert updated.email == "new@example.com"

@pytest.mark.asyncio
async def test_change_user_status(user_repo):
    user = await user_repo.create_user("status@example.com", "pass")
    result = await user_repo.change_user_status(user.id, False)
    assert "deactivated" in result