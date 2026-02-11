from users import schemas


def test_user_create():
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    user_create = schemas.UserCreate(**user_data)
    assert user_create.email == user_data["email"]
    assert user_create.password == user_data["password"]
