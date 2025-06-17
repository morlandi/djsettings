import os
import logging.config
from django.conf import settings


def setup_logging(verbose=None):
    """
    Use to set LOGGING settings variable;
    paramters:

        verbose: if True, force all loggers to use the console
        log_level: default value for log_level .. you can always apply a specific
                   level to individual loggers and/or handler below where appropriate

    Use AT THE VERY END of your settings file;
    if multiple files are involved (each one importing the other)
    use in the most external wrapper.

    from .logging import get_logging_config
    LOGGING = get_logging_config(
        verbose=True,
        log_level=LOG_LEVEL,
        log_root=LOG_ROOT,
        log_filename=LOG_FILENAME)
    """

    if verbose is None:
        verbose = settings.DEBUG

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

    if verbose:
        # make all loggers use the console.
        for logger in data["loggers"].values():
            handlers = logger["handlers"]
            if not "console" in handlers:
                handlers.append("console")

    logging.config.dictConfig(data)
