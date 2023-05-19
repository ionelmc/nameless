FROM postgres:15@sha256:8d45935fb783e72c871072e9eb72ee8c817a9eaf25c405b0e62526b14191368d

RUN groupmod --gid=1000 postgres \
 && usermod --uid=1000 postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
