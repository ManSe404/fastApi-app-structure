from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, UJSONResponse

from src.application.api import api_router
from src.application.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    async def not_found(request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
        )

    exception_handlers = {404: not_found}

    app = FastAPI(
        title="application",
        # version=metadata.version("application"),
        docs_url="/app/docs",
        redoc_url="/app/redoc",
        openapi_url="/app/openapi.json",
        exception_handlers=exception_handlers,
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router)

    return app
