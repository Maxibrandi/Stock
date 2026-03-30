FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copiamos los archivos de bloqueo de uv
COPY pyproject.toml uv.lock ./

# Instalamos las dependencias (sin instalar el proyecto aún)
RUN uv sync --frozen --no-cache

# Copiamos el resto del código
COPY . .

# Ejecutamos con uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]