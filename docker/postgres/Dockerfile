FROM postgres:15@sha256:6cc97262444f1c45171081bc5a1d4c28b883ea46a6e0d1a45a8eac4a7f4767ab

RUN groupmod --gid=1000 postgres \
 && usermod --uid=1000 postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
