FROM python:3.14-slim

WORKDIR /src

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.application:get_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]