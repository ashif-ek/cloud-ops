
FROM python:3.14-slim

# Python runtime settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install locked production dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source code
COPY app/ ./app/

# Run as a non-root user
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
