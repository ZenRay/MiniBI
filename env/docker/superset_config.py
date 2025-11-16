"""
Local Superset runtime overrides used by the compose setup.

This file is mounted into the container at `/app/superset_config.py` so
Superset's `superset.config` will import it and these values override
the defaults. We use this to point Superset to the Postgres metadata DB.

Do NOT commit sensitive credentials to a public repo; this file is meant
for local development. Alternatively keep credentials in `.env` and
interpolate them into this file at deploy time.
"""
import os

# Prefer environment variables when available (keeps secrets out of the file)
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'superset')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'superset_password_change_me')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'superset')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Keep file minimal; other overrides can be added if needed
