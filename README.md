# debug-statsig-client-init

Install:

- `just`
- `docker`
- `uv`

Env:

- Copy `.env.example` to `.env` and fill in your statsig api key.

Run:

- `just build`: Build everything.
- `just run-direct`: Run app directly via uv.
- `just run-docker`: Run app via docker compose.
- `just test`: Send a request to the running app.
