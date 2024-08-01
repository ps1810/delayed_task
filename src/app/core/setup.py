from collections.abc import AsyncGenerator
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any, Callable

import anyio
import fastapi
import redis.asyncio as redis
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


from .config import (
    AppSettings,
    EnvironmentOption,
    EnvironmentSettings,
    RedisQueueSettings,
    settings,
)
from .utils import queue

# -------------- queue --------------
async def create_redis_queue_pool() -> None:
    queue.pool = await create_pool(RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT))


async def close_redis_queue_pool() -> None:
    await queue.pool.close()  # type: ignore

# -------------- application --------------
async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


def lifespan_factory(
    settings: (
        AppSettings
        | RedisQueueSettings
        | EnvironmentSettings
    ),
) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    """Factory to create a lifespan async context manager for a FastAPI app."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        await set_threadpool_tokens()

        if isinstance(settings, RedisQueueSettings):
            await create_redis_queue_pool()

        yield

        if isinstance(settings, RedisQueueSettings):
            await close_redis_queue_pool()

    return lifespan


# -------------- application --------------
def create_application(
    router: APIRouter,
    settings: (
        AppSettings
        | RedisQueueSettings
        | EnvironmentSettings
    ),
    **kwargs: Any,
) -> FastAPI:
    """Creates and configures a FastAPI application based on the provided settings.

    This function initializes a FastAPI application and configures it with various settings
    and handlers based on the type of the `settings` object provided.
    The function configures the FastAPI application with different features and behaviors
    based on the provided settings. It includes setting up database connections, Redis pools
    for caching, queue, and rate limiting, client-side caching, and customizing the API documentation
    based on the environment settings.

    :param router : The APIRouter object containing the routes to be included in the FastAPI application.
    :type APIRouter

    :param settings:
        An instance representing the settings for configuring the FastAPI application.
        It determines the configuration applied:

        - AppSettings: Configures basic app metadata like name, description, contact, and license info.
        - RedisQueueSettings: Sets up event handlers for creating and closing a Redis queue pool.
        - EnvironmentSettings: Conditionally sets documentation URLs and integrates custom routes for API documentation
          based on the environment type.
    :type settings

    :param **kwargs: Additional keyword arguments passed directly to the FastAPI constructor.
    :type Any

    :rtype: FastAPI
    :return: FastAPI, A fully configured FastAPI application instance.
    """
    # --- before creating application ---
    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "contact": {"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
        }
        kwargs.update(to_update)

    if isinstance(settings, EnvironmentSettings):
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    lifespan = lifespan_factory(settings)

    application = FastAPI(lifespan=lifespan, **kwargs)
    application.include_router(router)

    if isinstance(settings, EnvironmentSettings):
        if settings.ENVIRONMENT == EnvironmentOption.LOCAL:
            docs_router = APIRouter()

            @docs_router.get("/docs", include_in_schema=False)
            async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/redoc", include_in_schema=False)
            async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
                return get_redoc_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/openapi.json", include_in_schema=False)
            async def openapi() -> dict[str, Any]:
                out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
                return out

            application.include_router(docs_router)

        return application