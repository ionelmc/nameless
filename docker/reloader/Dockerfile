# syntax=docker/dockerfile:1
FROM ubuntu:latest@sha256:353675e2a41babd526e2b837d7ec780c2a05bca0164f7ea5dbbd433d21d166fc
# Notes:
# - Debian-based images don't have docker tooling
# - Alpine-based images don't have fswatch (inotifywait only supports Linux filesystems)
# - Official Docker images are all Alpine-based

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
