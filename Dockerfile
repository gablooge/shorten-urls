# this allows dockerfile to *know* about build arguments

FROM python:3.11.6-alpine as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps build-base musl-dev postgresql-dev libffi-dev python3-dev cargo

RUN apk add --no-cache postgresql-client

COPY . /mainapps

WORKDIR /mainapps

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry export --output requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD sh ./scripts/wait-and-setup-for-postgres.sh && python manage.py migrate && gunicorn --bind :8001 --workers 3 mainapps.wsgi

EXPOSE 8001
