# fastapi_tutorial

## Overview

This project is a FastAPI tutorial application with two main parts:

- A simple book management API in the project root (`main.py`, `model.py`, `database.py`, `create_table.py`, `project.py`).
- A user authentication API in the `auth/` folder with signup, login, password hashing, and JWT access token creation.

The project uses:

- FastAPI for API endpoints
- SQLAlchemy for ORM and database models
- MySQL as the database backend
- passlib with Argon2 for password hashing
- python-jose for JWT token creation

## Repository structure

- `main.py` - Root FastAPI app with book routes for CRUD-style operations.
- `project.py` - Alternate FastAPI example showing a simple book create endpoint using SQLAlchemy `model.py`.
- `database.py` - Database connection configuration for MySQL and session management.
- `model.py` - SQLAlchemy model for the `books` table.
- `create_table.py` - Creates database tables for the root app models.
- `auth/` - Authentication module folder.
  - `auth/main.py` - Auth API with `/signup` and `/login` routes.
  - `auth/models.py` - SQLAlchemy user model.
  - `auth/schemas.py` - Pydantic schemas for user creation and login.
  - `auth/utils.py` - Password hashing and verification utilities.
  - `auth/auth_database.py` - Separate database configuration used by auth models.
  - `auth/auth_table.py` - Table creation script inside the auth module.

## Setup

1. Create and activate your Python virtual environment.

```powershell
python -m venv myenv
myenv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirement.txt
```

3. Configure MySQL connection

Open `database.py` and `auth/auth_database.py` and update the following values if needed:

- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`

The current configuration uses:

- user: `root`
- password: `Mysql123#`
- host: `localhost`
- port: `3307`
- database: `fastapi_db`

> Create the `fastapi_db` database in MySQL before running the app.

4. Create tables

For the root app models:

```powershell
python create_table.py
```

For the auth module, run:

```powershell
python auth\auth_table.py
```

> Note: `auth/auth_table.py` currently imports `Base` from `database.py` instead of `auth/auth_database.py`. If you want auth tables to use the auth database configuration, you may need to update `auth/auth_table.py` accordingly.

## Run the APIs

### Run the book API app

```powershell
uvicorn main:app --reload
```

Then visit:

- `GET /books` - list books
- `POST /book` - add a book
- `GET /books/{book_id}` - read one book
- `PUT /books/{book_id}` - update a book
- `DELETE /books/{book_id}` - delete a book

### Run the auth API app

```powershell
uvicorn auth.main:app --reload
```

Then visit:

- `POST /signup` - register a new user
- `POST /login` - authenticate and receive a JWT bearer token

## Auth workflow

### Signup

Request body example:

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "MySecret123",
  "role": "user"
}
```

The flow in `auth/main.py`:

- Checks if the email already exists
- Hashes the password using `auth/utils.py`
- Saves the new user to the database
- Returns the new user record fields

### Login

Use `OAuth2PasswordRequestForm` to submit form data:

- `username`
- `password`

The auth flow:

- Finds user by `username`
- Verifies password with `auth/utils.py`
- Creates a JWT token using `jose.jwt`
- Returns `access_token` and `token_type`

## Key files explained

### `database.py`

Defines the SQLAlchemy engine, session factory, and `Base` metadata for root models.

### `auth/auth_database.py`

Defines a second SQLAlchemy engine and session factory for auth-related models. It also defines its own `Base`.

### `model.py`

Defines the `Book` ORM model for the `books` table.

### `auth/models.py`

Defines the `User` ORM model for the `users` table.

### `auth/schemas.py`

Defines request payload validation using Pydantic:

- `UserCreate`
- `UserLogin`

### `auth/utils.py`

Handles secure password hashing and verification using Argon2.

## Notes and improvements

- The auth app currently uses `SECRET_KEY = ""`, which should be set to a secure random value before production.
- The auth routes return a JWT, but they do not yet protect other endpoints with dependency-based authentication.
- `auth/auth_table.py` and `create_table.py` both create tables; ensure they target the correct database metadata.
- The root `project.py` is a supplementary example showing one route and SQLAlchemy usage.

## Example usage

### Create a book

```powershell
curl -X POST "http://127.0.0.1:8000/book" -H "Content-Type: application/json" -d "{\"id\": 5, \"title\": \"New Book\", \"author\": \"Author\", \"publish_date\": \"2026\"}"
```

### Signup a user

```powershell
curl -X POST "http://127.0.0.1:8000/signup" -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"email\": \"admin@example.com\", \"password\": \"Admin123!\", \"role\": \"admin\"}"
```

### Login a user

```powershell
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=Admin123!"
```

## Dependencies

Installed libraries are declared in `requirement.txt`:

- `fastapi`
- `uvicorn`
- `SQLAlchemy`
- `pymysql`
- `passlib[argon2]`
- `python-jose[cryptography]`
- `python-multipart`
- `pydantic[email]`
