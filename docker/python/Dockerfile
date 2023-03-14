# syntax=docker/dockerfile:1
FROM buildpack-deps:22.04-scm@sha256:309fa57d4ff4c368763213a7e066d1b87cc15fe0949c124f3a7ed8430c4bcd1c as deps

ARG TZ=UTC

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list \
 && curl -fsSL11 'https://www.postgresql.org/media/keys/ACCC4CF8.asc' | apt-key add - \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-dev python3-distutils-extra \
        python-is-python3 \
        libpq-dev=15.* libpq5=15.* \
        libgdal-dev \
        libtiff-dev libjpeg-dev libzip-dev libfreetype-dev \
        libwebp-dev tcl-dev tk-dev libffi-dev \
        libmemcached-dev zlib1g-dev libpcre3-dev \
        build-essential git sudo ca-certificates

RUN bash -o pipefail -c "curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | \
    python - --no-cache --disable-pip-version-check --upgrade pip==23.0.1 setuptools==67.3.3"

# This intents to be the sole Dockerfile for the project so allow building variants with different or no dependencies.
COPY requirements/*.txt /requirements/
ARG REQUIREMENTS
ARG CPUCOUNT=1
RUN --mount=type=cache,target=/root/.cache set -x \
 && mkdir /deps \
 && if [ -n "$REQUIREMENTS" ] \
  ; then python -mpip wheel --wheel-dir=/deps/wheels -r requirements/$REQUIREMENTS.txt \
 && ls -al /deps/wheels \
  ; else echo 'No REQUIREMENTS defined!' \
  ; fi


##################################
##################################
FROM buildpack-deps:22.04@sha256:9a5858bbf22b934014c6d0cacb9e2e8281868a5315445da65574541a919dba32 as certs
##################################
ARG SERVER_NAME="localhost"
RUN mkdir /certs \
 && openssl req -x509 -nodes -newkey rsa:4096 -sha256 \
                -out /certs/fullchain.pem -keyout /certs/privkey.pem \
                -subj "/CN=$SERVER_NAME"

#################
#################
FROM ubuntu:22.04@sha256:2adf22367284330af9f832ffefb717c78239f6251d9d0f58de50b86229ed1427
#################
RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

ARG TZ=Europe/Bucharest
ENV TZ=$TZ
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl software-properties-common gpg-agent \
 && echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list \
 && curl -fsSL11 'https://www.postgresql.org/media/keys/ACCC4CF8.asc' | apt-key add - \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        strace ltrace gdb lsof locate net-tools htop iputils-ping dnsutils \
        nano vim tree less telnet \
        socat byobu \
        graphviz \
        dumb-init \
        libpq5=15.* postgresql-client-15 \
        python3-dbg python3-distutils python3-distutils-extra \
        python-is-python3 \
        libmemcached11 libpcre3 \
        sudo ca-certificates \
        nginx \
        gdal-bin python3-gdal



RUN bash -o pipefail -c "curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | \
    python - --no-cache --disable-pip-version-check --upgrade pip==23.0.1 setuptools==67.3.3"

RUN --mount=type=bind,from=deps,src=/deps,target=/deps set -x \
 && if [ -e /deps/wheels ] \
  ; then pip install --force-reinstall --ignore-installed --upgrade --no-index --no-deps /deps/wheels/* \
  ; else echo 'No wheels built!' \
  ; fi

# Adds a new user named python and add it to the list of sudoers. Will be able to call sudo without the password.
# This is more geared to development (eg: match user's UID) than production (where you shouln't need any sudo/home).
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd --gid $GROUP_ID app \
 && useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home app \
 && echo "app ALL=(ALL) NOPASSWD:ALL" | tee -a /etc/sudoers

RUN mkdir -p /app /var/app/logs /var/app/static /var/app/run /etc/app \
 && chown -R app:app /app /var/app/logs /var/app/run

ENV PYTHONPATH=/app/src
RUN echo /app/src > $(python -c 'print(__import__("sysconfig").get_path("purelib"))')/app.pth

RUN ln -sf /proc/self/fd/2 /var/app/logs/error.log \
 && ln -sf /proc/self/fd/1 /var/app/logs/access.log

COPY src /app/src

ENV PYTHONUNBUFFERED=x
ENV PYTHONFAULTHANDLER=x

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
ARG DJANGO_SECRET_KEY="n/a"
ARG SERVER_NAME="localhost"

WORKDIR /app

COPY docker/python/entrypoint.sh /
COPY docker/python/uwsgi.ini /etc/app/
COPY docker/python/worker.ini /etc/app/
COPY docker/python/nginx.conf /etc/app/
COPY docker/python/nginx.site /tmp/
COPY docker/python/yacron.yml /etc/app/
COPY --from=certs /certs/* /etc/app

ADD https://ssl-config.mozilla.org/ffdhe2048.txt /etc/app/dhparam

ARG SERVER_NAME="localhost"
RUN envsubst \$SERVER_NAME < /tmp/nginx.site > /etc/app/nginx.site
RUN cp /etc/app/fullchain.pem /etc/app/chain.pem \
 && ln -sf /etc/app/nginx.conf /etc/nginx/nginx.conf \
 && cp /etc/nginx/mime.types /etc/app \
 && chmod -R go+r /etc/app \
 && cp -r /etc/app /etc/app-defaults

ARG DJANGO_COLLECTSTATIC
RUN set -x \
 && if [ -n "$DJANGO_COLLECTSTATIC" ] \
  ; then __strict_env__=false django-admin collectstatic --noinput --clear -v0 \
  ; fi