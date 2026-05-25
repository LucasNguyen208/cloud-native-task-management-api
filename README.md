
# Cloud-Native Task Management API

A Flask-based task management REST API with JWT authentication, role-based access control, task assignment, database migrations, and Docker deployment.

## Features

- JWT authentication with protected routes
- Role-based access control (`admin`, `manager`, `user`)
- Task CRUD operations with assignment support
- Validation for auth and task payloads
- Swagger UI documentation via Flasgger at `/apidocs/`
- MySQL persistence with Alembic migrations
- Docker Compose deployment with automatic migration and seeding

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ for local development
- Git

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cloud-native-task-management-api.git
   cd cloud-native-task-management-api
   ```

2. Create a `.env` file with the required environment variables.

3. Start the application with Docker Compose:
   ```bash
   docker compose up --build
   ```

   The API container will run migrations and seed the default roles automatically.

## Running Locally Without Docker

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   source .venv/bin/activate      # macOS/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the required environment variables.

4. Set the Flask application entrypoint:
   ```bash
   set FLASK_APP=run.py          # Windows
   export FLASK_APP=run.py       # macOS/Linux
   ```

5. Apply database migrations:
   ```bash
   flask db upgrade
   ```

6. Seed default roles:
   ```bash
   python seed.py
   ```

7. Start the application:
   ```bash
   python run.py
   ```

## API Base URL

- Local development: `http://localhost:5000`
- Swagger UI: `http://localhost:5000/apidocs/`
- Health endpoint: `GET /`

## Authentication Endpoints

All authentication routes are mounted under `/api/auth`.

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate and retrieve a JWT
- `GET /api/auth/profile` - Get the authenticated user profile
- `GET /api/auth/admin` - Admin-only access test endpoint

### Registration Validation

- `username`: required, 3-50 characters
- `email`: required, must be valid
- `password`: required, minimum 8 characters

## Task Endpoints

Task routes are mounted under `/api/tasks` and require a valid JWT.

- `POST /api/tasks` - Create a new task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/<task_id>` - Get a single task
- `PUT /api/tasks/<task_id>` - Update a task
- `DELETE /api/tasks/<task_id>` - Delete a task

### Task Payloads

- `title` (required for creation): 3-255 characters
- `description` (optional): up to 1000 characters
- `status` (optional): one of `todo`, `in_progress`, `done`
- `assigned_to` (optional): user ID

### Task Permissions

- Admin users can update or delete any task
- Task creators can update or delete their own tasks
- Other authenticated users cannot modify tasks they do not own

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

The `api` container uses `entrypoint.sh` to wait for MySQL, run migrations, seed roles, and start the application.

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
│   ├── config.py
│   ├── errors/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── handlers.py
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
│   ├── services/
│   ├── utils/
│   │   └── db_helpers.py
│   └── validators/
│       ├── auth_validators.py
│       └── task_validators.py
├── migrations/
├── scripts/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
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
