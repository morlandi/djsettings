import json
import logging
from django.test import TransactionTestCase


class SampleTestCase(TransactionTestCase):

    def test1(self):
        self.assertTrue(True)

    def test_settings_and_logging(self):
        from main.settings.list_main_settings import list_main_settings
        main_settings = list_main_settings()
        print(json.dumps(main_settings, indent=2))

        logger = logging.getLogger("myapp")
        print("LEVEL:", logger.getEffectiveLevel())
        print("HANDLERS:", logger.handlers)
        print("PROPAGATE:", logger.propagate)
        for h in logger.handlers:
            print("  ->", h, h.level)
        logger._cache.clear()
        logger.debug('DEBUG message')
        logger.info('INFO message')
        logger.warning('WARNING message')
        logger.error('ERROR message')
