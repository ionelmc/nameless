FROM postgres:18@sha256:1ffc019dae94eca6b09a49ca67d37398951346de3c3d0cfe23d8d4ca33da83fb

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
