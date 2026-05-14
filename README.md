# Cloud-Native Task Management API

A robust, cloud-native task management REST API built with Flask, MySQL, and Docker. This project demonstrates DevOps practices including containerization, database migrations, and scalable architecture.

## Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access control (RBAC)
- **Task Management**: Create, read, update, and delete tasks with status tracking
- **Role-Based Permissions**: Admin and user roles with different access levels
- **Database Migrations**: Alembic for version-controlled database schema changes
- **Containerized Deployment**: Docker and Docker Compose for easy setup and deployment
- **RESTful API**: Well-structured endpoints following REST principles

## Prerequisites

- Docker and Docker Compose
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/cloud-native-task-management-api.git
   cd cloud-native-task-management-api
   ```

2. **Start the services:**
   ```bash
   docker compose up --build
   ```

3. **Run database migrations:**
   ```bash
   docker compose exec api flask db upgrade
   ```

4. **Seed the database (optional):**
   ```bash
   docker compose exec api python seed.py
   ```

## Usage

The API will be available at `http://localhost:5000`.

### API Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

#### Tasks (requires authentication)
- `GET /tasks` - Get all tasks (admin: all tasks, user: own tasks)
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

### Example API Usage

```bash
# Register a user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123", "role": "user"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Create a task (include JWT token in Authorization header)
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "Sample Task", "description": "This is a sample task", "status": "pending"}'
```

## Development

### Running Tests
```bash
docker compose exec api python -m pytest tests/
```

### Database Schema
The application uses MySQL with the following main tables:
- `users` - User accounts
- `roles` - User roles (admin, user)
- `tasks` - Task records

### Environment Variables
Key environment variables (configured in docker-compose.yml):
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- `JWT_SECRET_KEY`, `SECRET_KEY`

## Project Structure

```
cloud-native-task-management-api/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── config.py
│   ├── extensions/
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
│   └── services/
├── migrations/
├── scripts/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as a personal DevOps learning project
- Inspired by modern cloud-native application patterns
