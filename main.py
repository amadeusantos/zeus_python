from typing import Type

from fastapi import FastAPI
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

from src.config import envSettings
from src.api.exceptions import CoreException
from src.api.user.routers import router as user_router
from src.api.role.routers import router as role_router
from src.api.auth.routers import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)

register_tortoise(
    app,
    db_url=envSettings.DATABASE_URL,
    modules={"models": ["src.infrastructure.persistence.tortoise_orm.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.exception_handler(CoreException)
async def service_exception_handler(_, exc: CoreException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.get("/health")
async def health():
    return {"status": "ok"}
