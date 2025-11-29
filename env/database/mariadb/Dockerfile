# Simple MariaDB image wrapper
# Based on the official MariaDB image. Use this Dockerfile only if you
# need to extend or add custom configuration/initialization scripts.

FROM mariadb:10.6

# Set default environment variables (can be overridden by docker-compose/.env)
ENV MARIADB_ROOT_PASSWORD=${MARIADB_ROOT_PASSWORD:-root}
ENV MARIADB_DATABASE=${MARIADB_DATABASE:-superset}
ENV MARIADB_USER=${MARIADB_USER:-superset}
ENV MARIADB_PASSWORD=${MARIADB_PASSWORD:-superset}

# Copy optional custom configuration (if present)
# Put your custom my.cnf in this directory and it will be copied into the image.
COPY ./my.cnf /etc/mysql/conf.d/my.cnf

# Copy optional init SQL scripts (placed in /docker-entrypoint-initdb.d are executed at first startup)
COPY ./init.sql /docker-entrypoint-initdb.d/01-init.sql

VOLUME ["/var/lib/mysql"]
EXPOSE 3306

# Use upstream entrypoint/cmd; we don't override it to preserve initialization behavior
CMD ["mysqld"]
