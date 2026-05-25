from app.models.user import User


def create_and_login(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "task_user",
            "email": "task@test.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/api/auth/login", json={"email": "task@test.com", "password": "password123"}
    )

    with client.application.app_context():
        user = User.query.filter_by(email="task@test.com").first()

    return (login.json["access_token"], user.id)


def test_create_task_success(client):

    token, user_id = create_and_login(client)

    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "description": "Testing",
            "status": "todo",
            "assigned_to": user_id,
        },
    )

    assert response.status_code == 201


def test_get_tasks(client):

    token, _ = create_and_login(client)

    response = client.get("/api/tasks", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200


def test_get_tasks_without_token(client):

    response = client.get("/api/tasks")

    assert response.status_code == 401


def test_create_task_missing_title(client):

    token, user_id = create_and_login(client)

    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "Missing title", "status": "todo", "assigned_to": user_id},
    )

    assert response.status_code == 400


def test_create_task_invalid_status(client):

    token, user_id = create_and_login(client)

    response = client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Invalid",
            "description": "Testing",
            "status": "wrong",
            "assigned_to": user_id,
        },
    )

    assert response.status_code == 400


def test_get_non_existing_task(client):

    token, _ = create_and_login(client)

    response = client.get(
        "/api/tasks/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def create_task(client):

    token, user_id = create_and_login(client)

    client.post(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Task",
            "description": "Testing",
            "status": "todo",
            "assigned_to": user_id,
        },
    )

    response = client.get("/api/tasks", headers={"Authorization": f"Bearer {token}"})

    return (token, response.json[0]["id"])


def test_update_task_success(client):

    token, task_id = create_task(client)

    response = client.put(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated"},
    )

    assert response.status_code == 200


def test_update_invalid_status(client):

    token, task_id = create_task(client)

    response = client.put(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "wrong"},
    )

    assert response.status_code == 400


def test_delete_task_success(client):

    token, task_id = create_task(client)

    response = client.delete(
        f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def register_and_login(client, username, email):

    client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": "password123"},
    )

    login = client.post(
        "/api/auth/login", json={"email": email, "password": "password123"}
    )

    return login.json["access_token"]


def test_creator_can_update_task(client):

    token, task_id = create_task(client)

    response = client.put(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Creator Updated"},
    )

    assert response.status_code == 200


def test_other_user_cannot_update(client):

    creator_token, task_id = create_task(client)

    another_token = register_and_login(client, "another", "another@test.com")

    response = client.put(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {another_token}"},
        json={"title": "Hack"},
    )

    assert response.status_code == 403


def test_other_user_cannot_delete(client):

    creator_token, task_id = create_task(client)

    another_token = register_and_login(client, "delete_user", "delete@test.com")

    response = client.delete(
        f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {another_token}"}
    )

    assert response.status_code == 403
