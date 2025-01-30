import time
from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware


from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from .logger import base_logger
from starlette.middleware.base import _StreamingResponse
from .routers.auth_router import auth_router
from .routers.reg_log_router import reg_log_router
from .routers.user_router import user_router
from .routers.ui_router import ui_router


def get_application() -> FastAPI:
    application = FastAPI(root_path="/auth")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(ui_router)
    application.include_router(auth_router)
    application.include_router(reg_log_router)
    application.include_router(user_router)
    return application


app = get_application()


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    log_string = ""
    client_ip = f"user_ip: {request.client.host}" if request.client else ""
    log_string += f"Request: {request.method} {request.url}, {client_ip}\n"
    cookies = request.cookies
    if cookies:
        log_string += f"Request Cookies: {cookies}\n"
    body = await request.body()
    if body:
        log_string += f"Request Body: \n{body.decode()}\n"
    query_params = request.query_params
    if query_params:
        log_string += f"Query Parameters: {query_params}\n"
    start = time.monotonic()
    response: _StreamingResponse = await call_next(request)
    log_string += f"Response Status Code: {response.status_code}\n"
    elapsed_time = time.monotonic() - start
    log_string += f"Request Time: {elapsed_time:.4f} seconds\n"
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    response.headers["Content-Length"] = str(len(response_body))
    if not any(
        route in request.url.path for route in ["docs", "openapi.json", "ui/"]
    ):
        if 200 <= response.status_code <= 399:
            log_string += f"Response result: {response_body.decode()}\n"
            base_logger.info(f"Info about request:\n{log_string}")
        else:
            log_string += f"Response result: {response_body.decode()}\n"
            base_logger.error(f"Info about request:\n{log_string}")
    return Response(
        content=response_body,
        status_code=response.status_code,
        media_type=response.media_type,
        headers=dict(response.headers),
    )


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="FastAPI API documentation"
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)
