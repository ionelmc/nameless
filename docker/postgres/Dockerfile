FROM postgres:15@sha256:bab8d7be6466e029f7fa1e69ff6aa0082704db330572638fd01f2791824774d8

RUN groupmod --gid=1000 postgres \
 && usermod --uid=1000 postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
