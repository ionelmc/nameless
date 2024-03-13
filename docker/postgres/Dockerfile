FROM postgres:15@sha256:08ababf6ea4e32158b90673bc409302b3c4c38eb9aca71890966f2d28115d82f

RUN groupmod --gid=1000 postgres \
 && usermod --uid=1000 postgres

COPY extra-users.sh /docker-entrypoint-initdb.d/
