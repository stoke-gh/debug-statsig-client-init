import os
from contextlib import contextmanager
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from repro.router import router

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@contextmanager
def lifecycle(app: FastAPI) -> Generator[None, None, None]:
    from statsig import statsig

    api_key = os.getenv("STATSIG_API_KEY_SECRET")
    if api_key is None:
        raise ValueError("STATSIG_API_KEY_SECRET is not set")
    statsig.initialize(api_key)

    yield

    statsig.shutdown()


def build_app() -> FastAPI:
    app = FastAPI(lifecycle=lifecycle)
    add_middleware(app)
    app.include_router(router)
    return app
