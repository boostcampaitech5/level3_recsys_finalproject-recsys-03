import sys
from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from src.log.logger import get_fastapi_logger


def add_exception_handler(app: FastAPI):
    api_logger = get_fastapi_logger()

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        exception_type, exception_value, exception_traceback = sys.exc_info()
        exception_name = getattr(exception_type, "__name__", None)
        api_logger.warning("unhandled_exception_handler was called")
        api_logger.error("[%s] 500 Internal Server Error <%s : %s>", request.method, exception_name, exception_value)

        return PlainTextResponse(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
