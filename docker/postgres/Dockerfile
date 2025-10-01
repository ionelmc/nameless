FROM postgres:18@sha256:67a7c384da54fc55a3b5ad38e9853b76003603d12732c90af368b31bb1f2517f

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
