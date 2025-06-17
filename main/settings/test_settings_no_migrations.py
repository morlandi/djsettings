# -*- coding: utf-8 -*-
print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.test_settings_no_migrations")
from .test_settings import *


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None
        # return "notmigrations"


MIGRATION_MODULES = DisableMigrations()
