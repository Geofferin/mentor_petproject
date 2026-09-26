FROM python:3.14.1-slim AS builder
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /src
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .

FROM python:3.14.1-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/src/.venv/bin:$PATH"
WORKDIR /src
COPY --from=builder /src /src
EXPOSE 8000
CMD ["uvicorn", "src.application:get_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]