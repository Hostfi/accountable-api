# Accountable API

A FastAPI backend for the Accountable application, using Supabase for data storage and Clerk for authentication.

## Architecture

The application follows a layered architecture pattern:

### API Layers

1. **Endpoints** (`app/api/endpoints/`)
   - HTTP/REST interface layer
   - Handles request/response formatting
   - Input validation and error responses
   - Routes requests to appropriate managers/services
   - Example: `users.py` defines REST endpoints for user operations

2. **Managers** (`app/managers/`)
   - Business logic and database operations
   - Direct interaction with Supabase
   - CRUD operations and data transformations
   - Example: `user_manager.py` handles user data persistence

3. **Services** (`app/services/`)
   - Complex business operations
   - Orchestrates multiple managers
   - Handles caching and cross-cutting concerns
   - Example: `user_service.py` manages cached user operations

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management
- [Railway CLI](https://docs.railway.app/develop/cli) for local development
- A Supabase project
- A Clerk account

## Setup

1. **Install Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install Railway CLI**
   ```bash
   # macOS
   brew install railway

   # Other platforms
   npm i -g @railway/cli
   ```

3. **Clone and Install Dependencies**
   ```bash
   git clone <repository-url>
   cd accountable-api
   poetry install
   ```

4. **Environment Setup**
   ```bash
   # Login to Railway
   railway login

   # Link to your Railway project
   railway link

   # Start a shell with the environment variables
   railway run poetry shell
   ```

## Development

1. **Activate Poetry Shell with Railway Environment**
   ```bash
   railway run poetry shell
   ```

2. **Run Development Server**
   ```bash
   # Inside the Poetry shell with Railway environment
   poetry run dev
   ```

   This will start the FastAPI server with hot reload enabled.

3. **Run Tests**
   ```bash
   poetry run test
   ```

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## Database Migrations

Migrations are managed through Supabase and stored in the `supabase/migrations` directory.

To apply migrations locally:
1. Ensure you're in the Poetry shell with Railway environment
2. Run the migrations through the Supabase dashboard or CLI

## Project Structure

```
accountable-api/
├── app/
│   ├── api/            # API routes and dependencies
│   ├── managers/       # Business logic and database operations
│   ├── schemas/        # Pydantic models
│   └── utils/          # Utility functions
├── tests/             # Test files
├── poetry.lock        # Lock file for dependencies
└── pyproject.toml     # Project configuration and dependencies
```

## Environment Variables

The following environment variables are required and managed through Railway:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service role key
- `CLERK_API_KEY`: Your Clerk API key
- `DATABASE_URL`: PostgreSQL connection string

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[License Type] - See LICENSE file for details
