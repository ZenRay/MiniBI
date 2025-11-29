"""
Safe Celery shutdown handler registered via sitecustomize.

This module is intentionally minimal: it imports the Celery worker shutdown
signal and registers a no-op handler that suppresses RuntimeError raised
during teardown. It does not overwrite or re-create the Celery `app` object.
"""
import logging

try:
    from celery.signals import worker_shutdown
except Exception:
    # If celery not installed in build-time, ignore — handler won't be registered.
    worker_shutdown = None

logger = logging.getLogger(__name__)


def _safe_shutdown(sender=None, **kwargs):
    try:
        logger.info("Safe worker_shutdown handler invoked for %s", sender)
    except RuntimeError as e:
        logger.warning("Suppressed RuntimeError during worker shutdown: %s", e)
    except Exception:
        logger.exception("Non-fatal error in safe shutdown handler")


if worker_shutdown is not None:
    worker_shutdown.connect(_safe_shutdown)
