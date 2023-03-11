FROM python:3.11

WORKDIR /app/src

ADD $(pwd)/../pyproject.toml $(pwd)/../poetry.lock /app
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-ansi --no-interaction --no-root

ADD $(pwd)/../src /app/src
ADD $(pwd)/../scripts /app/scripts
