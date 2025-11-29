"""
Local Superset runtime overrides used by the compose setup.

This file is mounted into the container at `/app/superset_config.py` so
Superset's `superset.config` will import it and these values override
the defaults. Prefer using environment variables for secrets.
"""
import os

# Prefer environment variables when available (keeps secrets out of the file)

# Allow an explicit env override (useful when deploying without a file):
# - `SUPERSET__SQLALCHEMY_DATABASE_URI` (Superset-style nested env)
# - or `SQLALCHEMY_DATABASE_URI` (direct)
SQLALCHEMY_DATABASE_URI = os.environ.get('SUPERSET__SQLALCHEMY_DATABASE_URI') or os.environ.get(
    'SQLALCHEMY_DATABASE_URI'
)

# If no explicit DSN is provided, assemble it from POSTGRES_* env vars.
if not SQLALCHEMY_DATABASE_URI:
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'superset')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'superset')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'superset')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# Secret key and home dir come from env as well (do not hardcode in repo)
SUPERSET_SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY')
SUPERSET_HOME = os.environ.get('SUPERSET_HOME') or os.environ.get('SUPERSET_WORKDIR') or '/app/superset_home'

# Additional lightweight overrides can be added here as needed.

# Export/alias the secret and home so Superset's config loader can pick them up
if SUPERSET_SECRET_KEY:
    SECRET_KEY = SUPERSET_SECRET_KEY

# Some deployments expect SUPERSET_HOME to be present in the config namespace
if SUPERSET_HOME:
    # Keep original env var but also expose as variable used by some runtime code
    SUPERSET_HOME = SUPERSET_HOME
