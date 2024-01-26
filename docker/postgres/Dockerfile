FROM postgres:15@sha256:89d430f5f7e680e67f81de534eb459a3b86afd818e3330d9b18d29a6b9ec98cd

RUN groupmod --gid=1000 postgres \
 && usermod --uid=1000 postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
