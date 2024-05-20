FROM postgres:15@sha256:4b4da96c37fefd6f28c3f58e7470bbc6d2cb34ac5641b9df7221d962eb4bc55d

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
