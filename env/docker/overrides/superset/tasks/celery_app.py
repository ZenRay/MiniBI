# Minimal override of superset.tasks.celery_app with a safer teardown.
# This file is mounted into /app/superset/tasks/celery_app.py so it
# shadows the installed package when PYTHONPATH includes /app.

from typing import Any

from celery.signals import task_postrun, worker_process_init

# Import the original superset create_app and extensions
from superset import create_app
from superset.extensions import celery_app, db

# Initialize flask app (same as upstream)
flask_app = create_app()

# Expose celery app for celery CLI
app = celery_app


@worker_process_init.connect
def reset_db_connection_pool(**kwargs: Any) -> None:  # pylint: disable=unused-argument
    with flask_app.app_context():
        db.engine.dispose()


@task_postrun.connect
def teardown(retval: Any, *args: Any, **kwargs: Any) -> None:
    """
    Safer teardown: guard session.commit/remove with try/except and
    ensure we don't raise when outside application context.
    """
    try:
        if flask_app.config.get("SQLALCHEMY_COMMIT_ON_TEARDOWN"):
            if not isinstance(retval, Exception):
                try:
                    db.session.commit()
                except Exception:
                    # swallow commit errors to avoid crashing worker
                    pass

        if not flask_app.config.get("CELERY_ALWAYS_EAGER"):
            try:
                db.session.remove()
            except RuntimeError:
                # This happens when there's no active app context; ignore.
                pass
            except Exception:
                # swallow any other errors during remove
                pass
    except Exception:
        # Extremely defensive: ensure teardown never raises
        pass
