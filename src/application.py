from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.v1 import router as v1_router
from src import exceptions


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(exceptions.NotFoundError)
    async def not_found(request: Request, exc: exceptions.NotFoundError):
        return JSONResponse(status_code=404, content={'detail': 'Not found'})

def include_routers(app: FastAPI):
    app.include_router(v1_router)

def get_app() -> FastAPI:
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    include_routers(app)
    register_exception_handlers(app)

    return app
