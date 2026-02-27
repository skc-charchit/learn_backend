from contextlib import asynccontextmanager

from fastapi import FastAPI

from learn_backend.app.api.v1.routers import routers
from learn_backend.app.core.config import settings
from learn_backend.app.core.database import init_db, seed_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up the application...")
    # init database (create tables)
    if not settings.SKIP_DB_INIT:  # add a setting to skip db init if needed
        init_db()

    # seed database with initial data (development/learning only)
    # Set SEED_DB=true in .env or os.environ to enable seeding
    if settings.DEBUG:  # or add a SEED_DB setting
        seed_db()

    yield
    # Shutdown code here
    print("Shutting down the application...")


app = FastAPI(
    app_name=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(routers)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
