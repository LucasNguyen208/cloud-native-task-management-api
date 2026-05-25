def test_register_requires_body(client):

    response = client.post("/api/auth/register", json={})

    assert response.status_code == 400


def test_register_success(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    assert response.json["message"] == "User registered successfully"


def test_register_duplicate(client):

    payload = {
        "username": "duplicate",
        "email": "duplicate@test.com",
        "password": "password123",
    }

    client.post("/api/auth/register", json=payload)

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 409


def test_login_success(client):

    register_payload = {
        "username": "login_user",
        "email": "login@test.com",
        "password": "password123",
    }

    client.post("/api/auth/register", json=register_payload)

    response = client.post(
        "/api/auth/login", json={"email": "login@test.com", "password": "password123"}
    )

    assert response.status_code == 200

    assert "access_token" in response.json


def test_login_invalid_password(client):

    response = client.post(
        "/api/auth/login", json={"email": "login@test.com", "password": "wrong"}
    )

    assert response.status_code == 401


def test_profile_requires_token(client):

    response = client.get("/api/auth/profile")

    assert response.status_code == 401
