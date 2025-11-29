MariaDB helper Dockerfile

This folder contains a small wrapper around the official MariaDB image that
lets you add custom configuration and initialization scripts for local testing
or CI.

Files
- `Dockerfile` - builds from `mariadb:10.6`, copies `my.cnf` and `init.sql` into the image.
- `my.cnf` - example MariaDB configuration fragment (placed into `/etc/mysql/conf.d`).
- `init.sql` - example initialization SQL executed on first startup (creates `superset` DB and user).

Usage
- You can reference the image directly in a compose file by building this directory:

  services:
    mariadb:
      build: ./env/database/mariadb
      image: local/mariadb:10.6
      env_file: ./env/superset/.env
      environment:
        - MARIADB_ROOT_PASSWORD=${POSTGRES_PASSWORD:-root}
        - MARIADB_DATABASE=${POSTGRES_DB:-superset}
        - MARIADB_USER=${POSTGRES_USER:-superset}
        - MARIADB_PASSWORD=${POSTGRES_PASSWORD:-superset}
      volumes:
        - mariadb_data:/var/lib/mysql
      ports:
        - "3306:3306"

Notes
- The official MariaDB image already supports `MARIADB_DATABASE`, `MARIADB_USER`, and
  `MARIADB_PASSWORD` environment variables for initial database/user creation. The provided
  `init.sql` is optional and demonstrates how to create objects at first start.
- For production use prefer using the official image directly and manage secrets with
  Docker secrets or a secret manager. Avoid committing real passwords into `.env` files in
  source control.
