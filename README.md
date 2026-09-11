# Vemalog

A simple vehicle management REST API built with **Python + FastAPI**.

I made this project while learning backend development, starting from basic Python/OOP CRUD and exploring FastAPI, databases, authentication, and API design.

## Features

* User registration & login
* JWT authentication
* Password hashing
* Vehicle CRUD
* User → Vehicle relationship
* Vehicle data validation
* Oil change tracking
* Maintenance mileage calculation

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* JWT
* pwdlib
* uv

## Project Structure

```text
Vemalog/
├── routers/
│   ├── users.py
│   └── vehicles.py
├── auth.py
├── config.py
├── database.py
├── helper.py
├── main.py
├── models.py
├── schemas.py
├── pyproject.toml
└── uv.lock
```

## Notes

This is a learning project, so the code and architecture may evolve as I learn more about backend development.