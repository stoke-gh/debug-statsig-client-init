# =============================================================================
# Builder image
# =============================================================================

ARG STATSIG_API_KEY_SECRET

FROM python:3.13-slim AS builder

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

# Set environment variables
ENV \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  PYTHONPATH="/app" \
  PYTHONUNBUFFERED=1 \
  STATSIG_API_KEY_SECRET=${STATSIG_API_KEY_SECRET}

WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Copy source code
COPY packages/ ./packages/
COPY src/ ./src/

# Install dependencies into .venv
RUN uv sync --frozen --no-cache --all-packages

# =============================================================================
# Final image
# =============================================================================

FROM python:3.13-slim

WORKDIR /

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/src /app/src

EXPOSE 8000
ENTRYPOINT ["/app/.venv/bin/repro"]
