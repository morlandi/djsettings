import os
import logging.config
from django.conf import settings


def setup_logging():
    """
    Used to setup logging with logging.config.dictConfig(),
    while the LOGGING variable has been excluded as follows:

        # Prevent Django from automatically applying the default logging configuration
        LOGGING_CONFIG = None

    The use of settings.LOGGING can be convenient in simple situations,
    but problematic in cases where `LOGGING` itself depends on values set in the settings.


    If settings.LOG_TO_CONSOLE is True, force all loggers to use the console
    """

    force_log_to_console = settings.LOG_TO_CONSOLE
    if force_log_to_console is None:
        force_log_to_console = settings.DEBUG

    assert settings.LOGGING_CONFIG is None, "Prevent Django from automatically applying the default logging configuration"
    log_level = settings.LOG_LEVEL
    log_filepath = os.path.join(settings.LOG_ROOT, settings.LOG_FILENAME)
    os.makedirs(settings.LOG_ROOT, exist_ok=True)

    data = {
        'version': 1,
        'disable_existing_loggers': False,
        "formatters": {
            "verbose": {"format": "%(asctime)s|%(levelname)s|%(name)s| %(message)s"},
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "logfile": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": 1024 * 1204 * 1,
                "backupCount": 10,
                "filename": log_filepath,
                "formatter": "verbose",
            },
        },
        'root': {
            'handlers': ['console'],
            'level': log_level,
        },
        'loggers': {
            'myapp': {
                'handlers': ['logfile', ],
                'level': log_level,
                'propagate': False,
            },
            "django": {
                "handlers": ["logfile", ],
                "level": "WARNING",
                "propagate": True,
            },
        },
    }

    if force_log_to_console:
        # make all loggers use the console.
        for logger in data["loggers"].values():
            handlers = logger["handlers"]
            if not "console" in handlers:
                handlers.append("console")

    logging.config.dictConfig(data)
