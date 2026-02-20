ARG VERSION=3.14

FROM python:${VERSION}-alpine AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apk add --no-cache \
        postgresql-dev \
        gcc \
        musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    apk del gcc musl-dev


FROM python:${VERSION}-alpine AS final

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
        postgresql-libs

COPY --from=Builder /py /py

ENV PATH="/py/bin:$PATH"

COPY . .

RUN adduser --disabled-password --no-create-home django-user
USER django-user

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]