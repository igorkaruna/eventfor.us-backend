FROM python:3.11-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export --output requirements.txt


FROM python:3.11-slim as builder

WORKDIR /src

COPY --from=requirements-stage /tmp/requirements.txt /src/
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
