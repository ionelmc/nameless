FROM postgres:16

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
