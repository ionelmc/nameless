# syntax=docker/dockerfile:1.4
FROM buildpack-deps:22.04-scm@sha256:44fd3f944013377caec06347436126c04837bbeebeffc6f1701f3ddd26f10b33 as deps

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
        python3-dev python3-distutils-extra \
        python-is-python3 \
        libpq-dev=15.* libpq5=15.* \
        libgdal-dev \
        libtiff-dev libjpeg-dev libzip-dev libfreetype-dev \
        libwebp-dev tcl-dev tk-dev libffi-dev \
        libmemcached-dev zlib1g-dev libpcre3-dev \
        build-essential git sudo ca-certificates
EOF
RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | python - --no-cache --disable-pip-version-check --upgrade \
    pip==24.0 setuptools==69.2.0
EOF

# This intents to be the sole Dockerfile for the project so allow building variants with different or no dependencies.
COPY requirements/*.txt /requirements/
ARG REQUIREMENTS
ARG CPUCOUNT=1
RUN --mount=type=cache,target=/root/.cache <<EOF bash
    set -eux
    mkdir /deps
    if [[ -n "$REQUIREMENTS" ]]; then
        python -mpip wheel --no-deps --require-hashes --wheel-dir=/deps/wheels --requirement=requirements/$REQUIREMENTS.txt
        ls -al /deps/wheels
    else
        echo 'No REQUIREMENTS defined!'
        exit 1
    fi
EOF

##################################
##################################
FROM buildpack-deps:22.04@sha256:f028439d1e21418883b8ea83670b1bb142aae932caa17602f4542cd33cb85094 as certs
##################################
ARG SERVER_NAME="localhost"
RUN mkdir /certs \
 && openssl req -x509 -nodes -newkey rsa:4096 -sha256 \
                -out /certs/fullchain.pem -keyout /certs/privkey.pem \
                -subj "/CN=$SERVER_NAME"

#################
#################
FROM ubuntu:22.04@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
#################
RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    apt-get install -y --no-install-recommends \
        curl software-properties-common gpg-agent
    echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main 15" > /etc/apt/sources.list.d/pgdg.list
    echo "deb http://nginx.org/packages/mainline/ubuntu/ jammy nginx" > /etc/apt/sources.list.d/nginx.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    curl http://nginx.org/keys/nginx_signing.key | gpg --dearmor > /etc/apt/trusted.gpg.d/nginx.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
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
        tzdata
EOF

ARG TZ=Europe/Bucharest

# Force a sensible default encoding (affects terminal output and filename handling).
# See: https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/uwsgi/
# Note that for en_US.UTF-8 you need to install and compile locales, seems overkill...
ENV LANG=C.UTF-8

ENV TZ=$TZ
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata
RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | python - --no-cache --disable-pip-version-check --upgrade \
    pip==24.0 setuptools==69.2.0
EOF

RUN --mount=type=bind,from=deps,src=/deps,target=/deps <<EOF bash
    set -eux
    if [[ -e /deps/wheels ]]; then
        pip install --force-reinstall --ignore-installed --upgrade --no-index --no-deps /deps/wheels/*
    else
        echo 'No wheels built!'
        exit 1
    fi
EOF
# Adds a new user named python and add it to the list of sudoers. Will be able to call sudo without the password.
# This is more geared to development (eg: match user's UID) than production (where you shouln't need any sudo/home).
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd --gid $GROUP_ID app \
 && useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home app \
 && echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV PYTHONUNBUFFERED=x
ENV PYTHONFAULTHANDLER=x

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

ARG DJANGO_SECRET_KEY="n/a"
ARG SERVER_NAME="localhost"

RUN mkdir -p /app /var/app/logs /var/app/static /var/app/run /etc/app /etc/app-defaults /etc/app-latest \
             /shared/$SERVER_NAME/etc /shared/$SERVER_NAME/logs \
 && chown -R app:app /app /var/app/logs /var/app/run

ENV PYTHONPATH=/app/src
# Using 'EOF' instead of EOF to prevent substitutions on $
RUN <<'EOF' bash
    set -eux
    pth_location=$(python -c 'print(__import__("sysconfig").get_path("purelib"))')
    mkdir -p $pth_location
    echo /app/src > $pth_location/app.pth
EOF
RUN ln -sf /proc/self/fd/2 /var/app/logs/error.log \
 && ln -sf /proc/self/fd/2 /shared/$SERVER_NAME/logs/error.log \
 && ln -sf /proc/self/fd/1 /shared/$SERVER_NAME/logs/access.log

COPY src /app/src
RUN python -mcompileall /app/src

WORKDIR /app

COPY docker/python/entrypoint.sh /
COPY docker/python/uwsgi.ini /etc/app-latest
COPY docker/python/worker.ini /etc/app-latest
COPY docker/python/nginx.conf /etc/app-latest
COPY docker/python/nginx.site /etc/app-latest
COPY docker/python/yacron.yml /etc/app-latest

COPY --from=certs --chmod=0644 /certs/* /etc/app-defaults

ARG SERVER_NAME="localhost"
RUN <<EOF bash
    set -euxo pipefail
    envsubst '\$SERVER_NAME' < /etc/app-latest/nginx.site | sponge /etc/app-latest/nginx.site
EOF
RUN cp /etc/app-defaults/fullchain.pem /etc/app-defaults/chain.pem \
 && ln -sf /etc/app/nginx.conf /etc/nginx/nginx.conf \
 && cp /etc/nginx/mime.types /etc/app-latest \
 && chmod -R go+r /etc/app

ARG DJANGO_COLLECTSTATIC
RUN <<EOF bash
    set -eux
    if [[ -n "$DJANGO_COLLECTSTATIC" ]]; then
        __strict_env__=false django-admin collectstatic --noinput --clear -v0
    fi
EOF

ENTRYPOINT ["/entrypoint.sh"]
