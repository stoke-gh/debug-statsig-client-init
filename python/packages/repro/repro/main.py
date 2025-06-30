import os

from gunicorn.app.base import BaseApplication

from repro.app import build_app


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None  # type: ignore
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)  # type: ignore

    def load(self):
        return self.application


def main():
    # Do the new stuff.
    host = "::"
    port = int(os.environ.get("PORT", 8000))
    bind = f"[{host}]:{port}"
    workers = int(os.environ.get("WORKERS", 4))
    worker_class = "uvicorn.workers.UvicornWorker"
    config = {
        "bind": bind,
        "workers": workers,
        "worker_class": worker_class,
        "capture_output": False,
        "enable_stdio_inheritance": True,
    }
    app = build_app()
    StandaloneApplication(app, config).run()
