import asyncio
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from .config import MODULE_NAME
from .db import Base, engine
from .exceptions import PesopolistException
from .log import logger
from .routes import object_router, report_router


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(object_router, prefix=f"/{MODULE_NAME}")
    application.include_router(report_router, prefix=f"/{MODULE_NAME}")

    return application


async def main(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        try:
            response = await call_next(request)
        except PesopolistException as e:
            response = ORJSONResponse(
                {"Error": e.description}, status_code=e.status_code
            )
        except BaseException:
            logger.error(f"{request.method} {request.url.path}")
            traceback.print_exc()
            return ORJSONResponse(
                {"Error": f"Unknown {MODULE_NAME} error"}, status_code=500
            )

        logger.info(f"{request.method} {request.url.path} {response.status_code}")

        return response


if __name__ == "src.app":
    app = create_application()
    asyncio.run(main(app))
