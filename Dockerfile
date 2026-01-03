# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /code/

RUN uv export --format requirements-txt > requirements.txt

# Stage 2: Final
FROM python:3.13

WORKDIR /code

COPY --from=builder /code/requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
