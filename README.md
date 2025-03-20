# Accountable API

A robust HTTP REST API built with [FastAPI](https://fastapi.tiangolo.com/) for the Accountable platform.

This API includes the following features:

- **REST API endpoints** - a set of REST API endpoints using standard, spec-compliant methods like `GET` & `POST`
- **Rate Limiting** - automatic prevention of abuse of your API, at configurable rates based on customizable identifiers
- **Caching** - persistence of API responses to reduce load and improve performance
- **Dependency Injection** - invert control and share common functionality across the API
- **OpenAPI Documentation** - automatically generated OpenAPI documentation
- **Type Hints** - well-defined requests and responses with Pydantic models and type hints
- **Environment Variables** - configuration using environment variables that can be set in a `.env` file

### 🛠️ Setup & Installation

Prerequisites:

- [Python 3.10](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Redis](https://redis.io/download)

1. Clone the repository

```bash
git clone https://github.com/hostfi/accountable-api.git
cd accountable-api
```

2. Create a Poetry virtual environment

```bash
poetry env use 3.10
```

Start a shell within the virtual environment

```bash
poetry shell
```

3. Install dependencies

```bash
poetry install
```

4. Run the application

First make sure to start a redis server with

```bash
redis-server
```

Then run the application with:

```bash
poetry run dev
```

You should now be able to access the API at http://localhost:8000 on your machine.

## 📃 API Documentation

FastAPI automatically generates OpenAPI documentation for the API. You can access the interactive documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔑 Environment Variables

Environment variables are managed through a `.env` file. See the example `.env` file in the repository for the required configurations.

## 💿 Technology Stack

Built with modern technologies:

- **FastAPI** - High-performance web framework for building APIs with Python
- **Python 3.10** - Modern Python version with latest features
- **Poetry** - Dependency management and packaging
- **Redis** - In-memory data store for caching and rate limiting

## 📝 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/) - Comprehensive guide for building and structuring FastAPI applications
