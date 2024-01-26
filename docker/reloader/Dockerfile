# syntax=docker/dockerfile:1
FROM ubuntu:22.04@sha256:e6173d4dc55e76b87c4af8db8821b1feae4146dd47341e4d431118c7dd060a74

# Note: this uses ubuntu as the base instead of a more lightweight image
# like alpine because fswatch ain't in alpine and we want to use it instead
# of inotifywait which only supports Linux
# (iow: to support Docker for Windows and other setups with strange storage)

RUN test -e /etc/apt/apt.conf.d/docker-clean # sanity check

RUN <<EOF bash
    set -euxo pipefail
    export DEBIAN_FRONTEND=noninteractive

    apt-get update
    apt-get install -y --no-install-recommends \
                    fswatch docker.io docker-compose-v2 dumb-init
EOF
WORKDIR /app

COPY start.sh /

ENTRYPOINT ["dumb-init"]
CMD ["/start.sh"]
