# djsettings
“Smart enough” layout for Django project settings ... but not “too smart”.



## Project layout

The project includes:

- a `main` folder where the project is stored
- a `myapp` folder containing a simple application
- `myapp` introduces the logger `logging.getLogger(‘myapp’)`, which will be used to verify behavior in the logging system
- a simple `runtests.py` script to run unit tests in a controlled and predictable manner (but without introducing additional dependencies)
- a local working folder `data` excluded from the repository

The default database is SQlite, specifically “./data/db/db.sqlite3,” so it is necessary to ensure that the folder “./data/db” exists, even if the database itself is not actually used.

```bash
mkdir ./data/db
```

Most of the settings proposed by Django are unused in this minimal project, and have been commented out.



## Settings files

The files relating to settings, collected in a single module `main.settings`, have the role described below.

### setting.py

Contains a list of all project defaults, and is normally included by other files that integrate it and/or provide overrides for certain variables.

### local.py

**Not normally included in the repository**, this is the file used locally to characterize the needs of the specific instance;

it will normally contain `DEBUG=False` (at least in production) and the specifications of the database used by the instance.

Minimal example:

```python
from main.settings.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*', ]

LOG_LEVEL = "DEBUG"
TRACE_SETTINGS_ENABLED = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": PROJECT_INSTANCE,
        "USER": PROJECT_INSTANCE,
        "PASSWORD": "*****************************", # See deployment
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

### test_settings.py

The `runtests.py` script refers to this script to set the appropriate settings when running unit tests.


### \_\_init\_\_.py

This is where the magic happens.

The default setting for the project, without applying any specific configuration, is `main.settings`, which involves executing `main/settings/__init__.py`, which in turn:

- imports main.settings.local.py under normal conditions
- unless it detects that the execution context is that of unit testing
- if it does not find `local.py`, it triggers an exception
- if desired, we can kindly provide a `local_example.py` as an example to start with

### extra_settings.py

Optionally imported at the end; they are an opportunity for the deployment system to set specific configurations on a per-instance base.

## Logging configuration

The use of settings.LOGGING can be convenient in simple situations, but problematic in cases where `LOGGING` itself depends on values set in the settings; a situation that can be useful in practice.

For this reason, we have chosen to disable “static” LOGGING:

file `main/settings/settings/py`:

```python
# Prevent Django from automatically applying the default logging configuration
LOGGING_CONFIG = None
```

postponing the logging configuration to the AppConfig.ready() method, which is executed when all settings have been fully loaded:

file `main/apps.py`:

```python
class MainAppConfig(AppConfig):

    name = "main"
    verbose_name = "main"
    _logging_configured = False

    def ready(self):
        if not self._logging_configured:
            setup_logging()
            self._logging_configured = True
```

being, for example:

file `main/settings/logging.py`

```python
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
```


As an additional aid, `setup_logging()` uses the settings.LOG_TO_CONSOLE variable
to optionally assign the `console` handler to all `loggers` to facilitate interactive debugging.
