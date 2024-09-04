# syntax=docker/dockerfile:1.9
FROM buildpack-deps:24.04-scm as deps

ARG TZ=UTC

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    echo "deb http://apt.postgresql.org/pub/repos/apt noble-pgdg main 16" > /etc/apt/sources.list.d/pgdg.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
        python3-dev \
        python-is-python3 \
        libpq-dev=16.* libpq5=16.* \
        libgdal-dev \
        libtiff-dev libjpeg-dev libzip-dev libfreetype-dev \
        libwebp-dev tcl-dev tk-dev libffi-dev \
        libmemcached-dev zlib1g-dev libpcre3-dev \
        build-essential git sudo ca-certificates
EOF

RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL 'https://bootstrap.pypa.io/get-pip.py' | python - --no-cache --disable-pip-version-check --upgrade --break-system-packages \
    uv==0.4.4
EOF

ENV CPUCOUNT=1
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN <<EOF bash
    set -eux
    # clear leftover user that the 24.04 image has
    userdel ubuntu || true
    groupadd --gid $GROUP_ID app
    useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home app
    echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
EOF

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
