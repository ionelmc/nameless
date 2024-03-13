# syntax=docker/dockerfile:1.4
FROM ubuntu:22.04@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e

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
