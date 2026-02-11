from core import security


def test_password_hashing():
    password = "mysecretpassword"
    hashed_password = security.create_hash(password)
    assert hashed_password != password
    assert security.verify_hash(password, hashed_password) == (True, None)
    assert security.verify_hash("wrongpassword", hashed_password) == (False, None)


def test_token_creation_decoding():
    subject = "user123"
    token = security.create_token(subject, companyid=1)
    decoded = security.decode_token(token)
    assert decoded is not None
    assert decoded.get("sub") == subject
    assert decoded.get("companyid") == "1"
