# Best Practices for Database Connections and Dependencies in FastAPI with SQLModel

This document outlines the best practices for setting up and managing database connections and dependencies in a FastAPI application using SQLModel.

## 1. Project Structure

A well-organized project structure is crucial for maintainability. Here's a recommended layout for your database-related code:

```
app/
├── core/
│   ├── database.py       # Database engine, session creation, and initialization
│   └── dependencies.py   # Dependency injection setup
├── models/
│   └── airport_model.py  # SQLModel table models
├── services/
│   └── airport_service.py  # Business logic and database interaction
└── main.py               # FastAPI application entry point
```

- **`core/database.py`**: This file is responsible for creating the database engine, the session maker, and the `init_db` function to create tables.
- **`core/dependencies.py`**: This file defines the FastAPI dependencies that will be used to inject the database session into your services and endpoints.
- **`models/`**: This directory contains all your SQLModel table models. Each model represents a table in your database.
- **`services/`**: The service layer encapsulates the business logic of your application. Services interact with the database through the session provided by the dependency injection system.
- **`main.py`**: The main application file where you bring everything together, including the FastAPI application instance, routers, and the application lifespan events.

## 2. Defining the Database Model

Use SQLModel to define your database tables. Create a separate file for each model in the `models/` directory.

**`models/airport_model.py`:**
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Airport(SQLModel, table=True):
    __tablename__ = "airports"

    id: Optional[int] = Field(default=None, primary_key=True)
    icao: str = Field(sa_column_kwargs={"unique": True})
    iata: Optional[str] = Field(default=None)
    name: str
    country: Optional[str] = Field(default=None)
    elevation_ft: Optional[int] = Field(default=None)
```

## 3. Creating and Managing Database Sessions

In `core/database.py`, set up the asynchronous engine and session management.

**`core/database.py`:**
```python
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.airport_model import Airport # Import your models

DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```
**Important:** Remember to import all your SQLModel models into this file so that `SQLModel.metadata.create_all` can discover and create the tables.

## 4. Setting up Dependencies

Use FastAPI's dependency injection system to provide database sessions to your services. This is configured in `core/dependencies.py`.

**`core/dependencies.py`:**
```python
from typing import Annotated
from fastapi import Depends
from app.services.airport_service import AirportService
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

def provide_airport_service(db_session: Annotated[AsyncSession, Depends(get_session)]) -> AirportService:
    """
    Provides an AirportService with a database session dependency.
    """
    return AirportService(session=db_session)

AirportServiceDep = Annotated[AirportService, Depends(provide_airport_service)]
```
This setup ensures that a new database session is created for each request and is properly closed after the request is completed.

## 5. Implementing the Service Layer

The service layer contains the business logic. It receives the database session through its constructor and uses it to interact with the database.

**`services/airport_service.py`:**
```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.airport_model import Airport 

class AirportService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_airport_data(self, icao: str):
        statement = select(Airport).where(Airport.icao == icao)
        result = await self.session.exec(statement)
        return result.first()
```

## 6. Application Startup and Lifespan

In your `main.py`, use the `lifespan` context manager to initialize the database when the application starts.

**`main.py`:**
```python
from fastapi import FastAPI
from app.core.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("startup fastapi")
    await init_db()
    yield
    # shutdown
    print("shutdown fastapi")

app = FastAPI(lifespan=lifespan)

# ... rest of your application
```

By following these best practices, you can build a robust and maintainable FastAPI application with clean separation of concerns and a reliable database connection management system.
