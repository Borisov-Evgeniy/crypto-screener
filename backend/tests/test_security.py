from backend.app.core.security import password_hasher


def test_hash_password_return_different_hashes(sample_password):
    hash1 = password_hasher.hasher(sample_password)
    hash2 = password_hasher.hasher(sample_password)
    assert hash1 != hash2
    assert hash1.startswith('$2b$')
    assert hash2.startswith('$2b$')

def test_verify_password_correct(sample_password):
    hashed = password_hasher.hasher(sample_password)
    assert password_hasher.verify_password(sample_password,hashed) is True

def test_verify_password_incorrect(sample_password):
    hashed = password_hasher.hasher(sample_password)
    assert password_hasher.verify_password("wrong_password",hashed) is False

def test_verify_password_with_different_hashes(sample_password):
    hashed1 = password_hasher.hasher(sample_password)
    hashed2 = password_hasher.hasher(sample_password)
    assert password_hasher.verify_password(sample_password, hashed1) is True
    assert password_hasher.verify_password(sample_password, hashed2) is True