#!/usr/bin/env bash
set -e
# Local copy of apache/superset docker-init.sh used by compose setups
# Bootstraps DB migrations, admin user and runs superset init

# If the upstream docker image provides /app/docker/docker-bootstrap.sh, run it
if [ -f /app/docker/docker-bootstrap.sh ]; then
    /app/docker/docker-bootstrap.sh
fi

ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"
if [ "${CYPRESS_CONFIG:-}" = "true" ]; then
    ADMIN_PASSWORD="general"
    export SUPERSET_TESTENV=true
    export POSTGRES_DB=superset_cypress
    export SUPERSET__SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://superset:superset@db:5432/superset_cypress
fi

echo "Applying DB migrations"
superset db upgrade

echo "Creating admin user (admin / ${ADMIN_PASSWORD})"
if [ "${CYPRESS_CONFIG:-}" = "true" ]; then
    superset load_test_users
else
    superset fab create-admin \
        --username admin \
        --email admin@superset.com \
        --password "${ADMIN_PASSWORD}" \
        --firstname Superset \
        --lastname Admin
fi

echo "Initializing Superset"
superset init

if [ "${SUPERSET_LOAD_EXAMPLES:-}" = "yes" ]; then
    echo "Loading example data"
    if [ "${CYPRESS_CONFIG:-}" = "true" ]; then
        superset load_examples --load-test-data
    else
        superset load_examples
    fi
fi
