FROM python:3.11 as prod

WORKDIR /app/src

ADD $(pwd)/../pyproject.toml $(pwd)/../poetry.lock /app
RUN pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-ansi --no-interaction --no-root

ADD $(pwd)/../src /app/src
ADD $(pwd)/../scripts /app/scripts

FROM prod as dev

RUN apt-get update && apt-get install entr
RUN poetry install --only=dev --no-root
