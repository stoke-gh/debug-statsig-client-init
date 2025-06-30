import os
import sys

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/v1")


# Print directly to stdout fd if needed, otherwise gunicorn may capture logs.
def do_print(msg: str) -> None:
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def simple_statsig() -> None:
    import requests
    from statsig_python_core import Statsig, StatsigOptions, StatsigUser

    do_print("simple_statsig: start")

    api_key = os.getenv("STATSIG_API_KEY_SECRET")
    if api_key is None:
        raise ValueError("api_key is not set")

    do_print(f"simple_statsig: api_key: ...{api_key[-5:]}")

    do_print("simple_statsig: sending post")

    requests.post(
        "https://api.statsig.com/v1/webhooks/event_webhook",
        json={
            "user": {
                "userID": "test-user-456",
            },
            "event": "test_statsig_event_requests",
        },
        headers={
            "Content-Type": "application/json",
            "Accept": "*/*",
            "STATSIG-API-KEY": api_key,
        },
    )

    do_print("simple_statsig: post done")

    do_print("simple_statsig: making options")

    options = StatsigOptions()
    options.environment = "production"

    do_print("simple_statsig: start init")

    client = Statsig(api_key, options)

    do_print("simple_statsig: client object built")

    # This line never completes. In gunicorn/uvicorn setup we see this error:
    # │ [2025-06-24 17:33:28 +0000] [1] [CRITICAL] WORKER TIMEOUT (pid:25)                                                                                                                                           │
    # │ [2025-06-24 17:33:29 +0000] [1] [ERROR] Worker (pid:25) was sent SIGKILL! Perhaps out of memory?
    # The box is definitely not out of memory and nothing else causes these errors.
    client.initialize().wait()

    # === IT NEVER GETS HERE ===

    do_print("simple_statsig: initialize done")

    client.log_event(
        user=StatsigUser(user_id="test-user-123"),
        event_name="test_statsig_event_native",
    )

    do_print("simple_statsig: log done")

    client.flush_events()

    do_print("simple_statsig: flush done")

    client.shutdown().wait()

    do_print("simple_statsig: shutdown done")


@router.get("/test")
async def test():
    simple_statsig()
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {"hello": "world"},
        },
    )
