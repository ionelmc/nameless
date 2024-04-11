FROM postgres:15@sha256:1e511882ab82b1fe6cb6411d340a0f300837605767d039a8b27eab6ed8581a89

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
