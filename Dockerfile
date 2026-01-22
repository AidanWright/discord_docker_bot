# Usar una imagen base de Python
FROM python:3.11-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Comando por defecto para ejecutar la app
CMD ["uv", "run", "src/discord-docker-bot/main.py"]
