# debug-statsig-client-init

Machine:

- Mac Apple Silicon

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
- `just tilt`: Run tilt commands with correct context set.

To setup tilt:

- Install `docker`, `tilt`, `kind`, `helm`, `kubectl`, `ctlptl`, `cilium`.
- First unset any k8s context you have:
  - `kubectl config unset current-context`
- Run `just tilt up`
  - The first execution will time out if you are creating the cluster for the
    first time. Cancel it after the helm repos are setup and the network is
    "waiting on connection to cluster".
  - Then run `just tilt up` again and things should complete.
