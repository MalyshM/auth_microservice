ARG UV_VER=latest
FROM python:3.12.8-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /srv

COPY .python-version /srv/.python-version
COPY pyproject.toml /srv/pyproject.toml
COPY uv.lock /srv/uv.lock
COPY Makefile /srv/Makefile
COPY .env /srv/.env

RUN uv sync --frozen --dev
ENV PATH="/srv/.venv/bin:$PATH"

COPY auth_microservice/ /srv/auth_microservice/

RUN make test

EXPOSE 8090

CMD ["uvicorn", "auth_microservice.src.main:app", "--host", "0.0.0.0", "--port", "8090"]