import os
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from myapp.app_logger import try_app_logger
from .trace import trace_settings
from .settings.logging import setup_logging


class MainAppConfig(AppConfig):

    name = "main"
    verbose_name = "main"
    _logging_configured = False

    def ready(self):
        if not self._logging_configured:
            setup_logging()
            self._logging_configured = True
        trace_settings()

        if os.environ.get("RUN_MAIN") is None:
            try_app_logger()
