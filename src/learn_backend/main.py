from fastapi import FastAPI

from learn_backend.app.api.v1.routers import routers
from learn_backend.app.core.config import settings

app = FastAPI(
    app_name=settings.APP_NAME,
    debug=settings.DEBUG,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(routers)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
