# Cloud-Native Task Management API

A task management REST API built with Flask, MySQL, JWT authentication, RBAC, and Docker. The project includes API documentation via Swagger, database migrations, and seeded role support.

## Features

- JWT-based authentication
- Role-based access control with `admin`, `manager`, and `user`
- Task CRUD endpoints
- Task assignment support
- Input validation for users and tasks
- Swagger UI documentation at `/apidocs/`
- MySQL database with Alembic migrations
- Docker Compose deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cloud-native-task-management-api.git
   cd cloud-native-task-management-api
   ```

2. Create a `.env` file with the required environment variables, or ensure your `docker-compose.yml` env file is configured.

3. Start the application with Docker Compose:
   ```bash
   docker compose up --build
   ```

   The container entrypoint automatically runs database migrations and seeds default roles.

## Running Locally Without Docker

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your database and JWT settings.

3. Apply database migrations:
   ```bash
   flask db upgrade
   ```

4. Seed default roles:
   ```bash
   python seed.py
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## API Base URL

- Local development: `http://localhost:5000`
- Swagger UI: `http://localhost:5000/apidocs/`
- Health endpoint: `GET /`

## Authentication Endpoints

All auth routes are mounted under `/api/auth`.

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate and retrieve a JWT
- `GET /api/auth/profile` - Get current user profile (requires token)
- `GET /api/auth/admin` - Admin-only endpoint (requires token)

### Registration Validation

- `username` must be 3-50 characters
- `email` must be valid and unique
- `password` must be at least 8 characters

## Task Endpoints

Task routes are mounted under `/api/tasks` and require a valid JWT.

- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/<task_id>` - Get a single task
- `PUT /api/tasks/<task_id>` - Update a task
- `DELETE /api/tasks/<task_id>` - Delete a task

### Task Fields

- `title` (required): 3-255 characters
- `description` (optional): up to 1000 characters
- `status` (optional): one of `todo`, `in_progress`, `done`
- `assigned_to` (optional): user ID

### Task Permissions

- Admins can update and delete any task
- Task creators can update/delete their own tasks
- Other users are forbidden from modifying tasks they do not own

## Example Requests

Register a user:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

Create a task:
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "Implement Swagger", "description": "Add API docs", "assigned_to": 1}'
```

## Environment Variables

Create a `.env` file or provide these values in your Compose environment file:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

## Docker Compose

The Docker Compose setup includes:

- `api`: Flask application exposed on port `5000`
- `db`: MySQL 8.4 database exposed on port `3307`

## Testing

Run tests inside the Docker container:
```bash
docker compose exec api python -m pytest tests/
```

## Project Structure

```text
cloud-native-task-management-api/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── config.py
│   ├── extensions/
│   │   └── __init__.py
│   ├── middleware/
│   │   └── rbac.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── role.py
│   │   ├── task.py
│   │   └── user.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── tasks.py
│   └── validators/
│       ├── auth_validators.py
│       └── task_validators.py
├── migrations/
├── scripts/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── run.py
└── seed.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a pull request

## License

This project is licensed under the MIT License.
