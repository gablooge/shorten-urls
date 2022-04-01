FROM python:3.10.2-alpine3.15

COPY . /hseer

RUN set -ex \
    && apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps build-base postgresql-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /hseer/requirements/base.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

RUN apk add --no-cache postgresql-client
WORKDIR /hseer

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

RUN chmod +x wait-for-postgres.sh
