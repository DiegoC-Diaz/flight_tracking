from fastapi import (
    FastAPI,
    Depends,  # Import Depends
)
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from app.core.database import init_db, get_session, close_db  # Import get_session and close_db
from contextlib import asynccontextmanager
from sqlmodel import select  # Import select
from sqlmodel.ext.asyncio.session import AsyncSession  # Import AsyncSession
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("startup fastapi")
    #await init_db()
    yield
    # shutdown
    await close_db()
    print("shutdown fastapi")
    


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root(session: AsyncSession = Depends(get_session)):
    """
    An example "Hello world" FastAPI route that also tests the database connection.
    """
    # Execute a simple query to test the session
    result = await session.execute(select(1))
    db_status = "connected" if result.scalar() == 1 else "error"

    return {"message": "Hello World", "database": db_status}


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
