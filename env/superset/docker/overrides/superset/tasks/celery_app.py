"""
Safe Celery shutdown handler override.

This module registers a harmless handler for the Celery worker shutdown
signal and explicitly suppresses RuntimeError exceptions that were being
raised during teardown in some Superset versions when the Flask
application context was already torn down. The handler does not attempt
to re-implement Superset internals; it merely ensures the shutdown
signal doesn't abort the worker process with an uncaught exception.
"""
import logging

from celery.signals import worker_shutdown

logger = logging.getLogger(__name__)


@worker_shutdown.connect
def superset_safe_worker_shutdown(sender=None, **kwargs):
    try:
        logger.info("Invoked safe Superset worker_shutdown handler for %s", sender)
        # Intentionally no-op; if original handlers raise RuntimeError
        # while the Flask app context is already gone, we swallow that
        # to avoid crashing the worker during orderly shutdown.
    except RuntimeError as e:
        logger.warning("Suppressed RuntimeError during worker shutdown: %s", e)
    except Exception as e:
        # Log other unexpected exceptions but don't re-raise during shutdown
        logger.exception("Non-fatal error in safe shutdown handler: %s", e)
