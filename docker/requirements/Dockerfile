# syntax=docker/dockerfile:1
FROM python:3.13-trixie@sha256:716cd434754a988d55cb51f6aecd68e29446773582b100b497e4ef999f4a7196

ARG TZ=UTC

# DEBIAN_FRONTEND=noninteractive exists to prevent tzdata going nuts.
# Maybe dpkg incorrectly detects interactive on buildkit containers?
RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    echo "deb http://apt.postgresql.org/pub/repos/apt trixie-pgdg main 18" > /etc/apt/sources.list.d/pgdg.list
    curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg
    apt-get update
    apt-get install -y --no-install-recommends \
        libpq-dev=18.* libpq5=18.* \
        libgdal-dev \
        libtiff-dev libjpeg-dev libzip-dev libfreetype-dev \
        libwebp-dev tcl-dev tk-dev libffi-dev \
        zlib1g-dev libpcre3-dev \
        build-essential git sudo ca-certificates
EOF

RUN <<EOF bash
    set -euxo pipefail
    curl -fsSL https://github.com/astral-sh/uv/releases/download/0.8.22/uv-installer.sh | XDG_BIN_HOME=/usr/local/bin sh
EOF

ENV CPUCOUNT=1
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN <<EOF bash
    set -eux
    groupadd --gid $GROUP_ID app
    useradd --uid $USER_ID --gid $GROUP_ID --shell /bin/bash --create-home app
    echo "app ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
EOF

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
