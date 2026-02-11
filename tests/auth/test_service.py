import asyncio

import auth.service as service


class FakeSession:
    def __init__(self) -> None:
        self.add_calls = []
        self.commit_called = False
        self.refresh_calls = []

    def add(self, obj) -> None:
        self.add_calls.append(obj)

    async def commit(self) -> None:
        self.commit_called = True

    async def refresh(self, obj) -> None:
        self.refresh_calls.append(obj)


class FakeUser:
    def __init__(self, email: str, hashed_password: str) -> None:
        self.email = email
        self.hashed_password = hashed_password


def test_authenticate_user_returns_none_when_missing_user(monkeypatch):
    async def fake_get_user_by_email(db, email: str):
        return None

    monkeypatch.setattr(service, "get_user_by_email", fake_get_user_by_email)

    db = FakeSession()
    result = asyncio.run(service.authenticate_user(db, "nope@example.com", "pw"))

    assert result is None
    assert db.add_calls == []
    assert db.commit_called is False
    assert db.refresh_calls == []


def test_authenticate_user_returns_none_when_password_invalid(monkeypatch):
    user = FakeUser("user@example.com", "hashed")

    async def fake_get_user_by_email(db, email: str):
        return user

    def fake_verify_hash(password: str, hashed_password: str):
        return False, None

    monkeypatch.setattr(service, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(service, "verify_hash", fake_verify_hash)

    db = FakeSession()
    result = asyncio.run(service.authenticate_user(db, user.email, "bad"))

    assert result is None
    assert db.add_calls == []
    assert db.commit_called is False
    assert db.refresh_calls == []


def test_authenticate_user_returns_user_without_rehash(monkeypatch):
    user = FakeUser("user@example.com", "hashed")

    async def fake_get_user_by_email(db, email: str):
        return user

    def fake_verify_hash(password: str, hashed_password: str):
        return True, None

    monkeypatch.setattr(service, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(service, "verify_hash", fake_verify_hash)

    db = FakeSession()
    result = asyncio.run(service.authenticate_user(db, user.email, "pw"))

    assert result is user
    assert db.add_calls == []
    assert db.commit_called is False
    assert db.refresh_calls == []


def test_authenticate_user_rehashes_password(monkeypatch):
    user = FakeUser("user@example.com", "old_hash")

    async def fake_get_user_by_email(db, email: str):
        return user

    def fake_verify_hash(password: str, hashed_password: str):
        return True, "new_hash"

    monkeypatch.setattr(service, "get_user_by_email", fake_get_user_by_email)
    monkeypatch.setattr(service, "verify_hash", fake_verify_hash)

    db = FakeSession()
    result = asyncio.run(service.authenticate_user(db, user.email, "pw"))

    assert result is user
    assert user.hashed_password == "new_hash"
    assert db.add_calls == [user]
    assert db.commit_called is True
    assert db.refresh_calls == [user]


def test_login_for_access_token_returns_none_when_auth_fails(monkeypatch):
    async def fake_authenticate_user(db, email: str, password: str):
        return None

    monkeypatch.setattr(service, "authenticate_user", fake_authenticate_user)

    db = FakeSession()
    result = asyncio.run(service.login_for_access_token(db, "user@example.com", "pw"))

    assert result is None


def test_login_for_access_token_returns_token(monkeypatch):
    user = FakeUser("user@example.com", "hashed")

    async def fake_authenticate_user(db, email: str, password: str):
        return user

    def fake_create_token(email: str):
        return f"token-for-{email}"

    monkeypatch.setattr(service, "authenticate_user", fake_authenticate_user)
    monkeypatch.setattr(service, "create_token", fake_create_token)

    db = FakeSession()
    result = asyncio.run(service.login_for_access_token(db, user.email, "pw"))

    assert result == "token-for-user@example.com"
