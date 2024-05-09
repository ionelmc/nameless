FROM postgres:15@sha256:1ebd963e5c598f944a4e9ba27de4c95289d663dcc73731025aa53c5254094d8f

RUN if which apk; then apk --no-cache add shadow; fi
ARG UID=1000
ARG GID=1000
RUN groupmod --gid=$GID postgres || true
RUN usermod --uid=$UID --gid=$GID postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
