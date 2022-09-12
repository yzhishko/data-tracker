import logging
import signal

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from data_tracker.server.dependencies.singletons import CryptoUpdateWorkerInstance
from data_tracker.server.model.exceptions.api_exception import APIException
from data_tracker.server.routes import router

_app = None


def handler(signum, frame):
    CryptoUpdateWorkerInstance.get().shutdown()


async def api_exception_handler(_: Request, exception: APIException):
    logging.getLogger().exception(exception.message)
    return JSONResponse(status_code=400, content={"detail": exception.message})


def _create_app():
    base_app = FastAPI()
    base_app.include_router(router)
    base_app.add_exception_handler(APIException, api_exception_handler)
    # Version the API
    return VersionedFastAPI(base_app, version_format='{major}', prefix_format='/app/v{major}')


async def asgi_create_app(scope, receive, send):
    global _app
    if _app is None:
        _app = _create_app()
        CryptoUpdateWorkerInstance.get().start()
        signal.signal(signal.SIGUSR1, handler)
    return await _app(scope, receive, send)
