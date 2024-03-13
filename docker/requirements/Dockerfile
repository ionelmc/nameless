# syntax=docker/dockerfile:1.4
FROM buildpack-deps:22.04-scm@sha256:44fd3f944013377caec06347436126c04837bbeebeffc6f1701f3ddd26f10b33 as deps

ARG TZ=UTC

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
    uv==0.1.18
EOF

ENV CPUCOUNT=1
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd --gid $GROUP_ID app \
 && useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home /app

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
