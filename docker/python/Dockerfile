# syntax=docker/dockerfile:1
FROM buildpack-deps:22.04-scm@sha256:85a724d0c2d43aedabd8a30ed5aaf8dfc783166a56dc879f7a0f892b65260e06 as deps

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list \
 && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg \
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
    python - --no-cache --disable-pip-version-check --upgrade pip==23.0.1 setuptools==67.6.0"

# This intents to be the sole Dockerfile for the project so allow building variants with different or no dependencies.
COPY requirements/*.txt /requirements/
ARG REQUIREMENTS
ARG CPUCOUNT=1
RUN --mount=type=cache,target=/root/.cache set -x \
 && mkdir /deps \
 && if [ -n "$REQUIREMENTS" ] \
  ; then python -mpip wheel --no-deps --require-hashes --wheel-dir=/deps/wheels --requirement=requirements/$REQUIREMENTS.txt \
 && ls -al /deps/wheels \
  ; else echo 'No REQUIREMENTS defined!' \
  ; fi


##################################
##################################
FROM buildpack-deps:22.04@sha256:7ecd6942c89d480af224b1b79d28a352884c61d9d8a566eb96fd06f29537afeb as certs
##################################
ARG SERVER_NAME="localhost"
RUN mkdir /certs \
 && openssl req -x509 -nodes -newkey rsa:4096 -sha256 \
                -out /certs/fullchain.pem -keyout /certs/privkey.pem \
                -subj "/CN=$SERVER_NAME"

#################
#################
FROM ubuntu:22.04@sha256:dfd64a3b4296d8c9b62aa3309984f8620b98d87e47492599ee20739e8eb54fbf
#################
RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl software-properties-common gpg-agent \
 && echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list \
 && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        strace ltrace gdb lsof locate net-tools htop iputils-ping dnsutils \
        nano vim tree less telnet socat byobu \
        rsync moreutils \
        graphviz \
        dumb-init \
        libpq5=15.* postgresql-client-15 \
        python3-dbg python3-distutils python3-distutils-extra \
        python3-gdal gdal-bin \
        python-is-python3 \
        libmemcached11 libpcre3 \
        sudo ca-certificates \
        nginx \
        rsync \
        tzdata

ARG TZ=Europe/Bucharest

# Force a sensible default encoding (affects terminal output and filename handling).
# See: https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/uwsgi/
# Note that for en_US.UTF-8 you need to install and compile locales, seems overkill...
ENV LANG=C.UTF-8

ENV TZ=$TZ
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata

RUN bash -o pipefail -c "curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | \
    python - --no-cache --disable-pip-version-check --upgrade pip==23.0.1 setuptools==67.6.0"

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

RUN mkdir -p /app /var/app/logs /var/app/static /var/app/run /etc/app /etc/app-defaults /etc/app-latest \
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
COPY docker/python/uwsgi.ini /etc/app-latest
COPY docker/python/worker.ini /etc/app-latest
COPY docker/python/nginx.conf /etc/app-latest
COPY docker/python/nginx.site /etc/app-latest
COPY docker/python/yacron.yml /etc/app-latest

COPY --from=certs /certs/* /etc/app-defaults

ARG SERVER_NAME="localhost"
RUN envsubst \$SERVER_NAME < /etc/app-latest/nginx.site | sponge /etc/app-latest/nginx.site
RUN cp /etc/app-defaults/fullchain.pem /etc/app-defaults/chain.pem \
 && ln -sf /etc/app/nginx.conf /etc/nginx/nginx.conf \
 && cp /etc/nginx/mime.types /etc/app-latest \
 && chmod -R go+r /etc/app

ARG DJANGO_COLLECTSTATIC
RUN set -x \
 && if [ -n "$DJANGO_COLLECTSTATIC" ] \
  ; then __strict_env__=false django-admin collectstatic --noinput --clear -v0 \
  ; fi
