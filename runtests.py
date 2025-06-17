#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

APP_LIST = [
    "myapp",
]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--verbosity", "-v", type=int, default=2)
    parser.add_argument(
        "--no-migrations",
        "-m",
        action="store_true",
        help="Skip migrations. (default: False)",
    )
    parser.add_argument(
        "--no-keepdb",
        action="store_true",
        help="Don't pass --keepdb option to TestRunner (default: False)",
    )

    args = parser.parse_args()
    verbosity = args.verbosity
    os.environ["DJANGO_TEST_RUNNER_VERBOSITY"] = str(verbosity)

    app_list = APP_LIST
    keepdb = True
    if args.no_keepdb:
        keepdb = False

    os.environ["DJANGO_SETTINGS_MODULE"] = (
        "main.settings.test_settings_no_migrations"
        if args.no_migrations
        else "main.settings.test_settings"
    )

    django.setup()

    # # Set log level based on verbosity
    # levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO]
    # loglevel = levels[min(len(levels) - 1, verbosity)]  # capped to number of levels
    # logging.disable(loglevel)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, keepdb=keepdb)
    failures = test_runner.run_tests(app_list)
    sys.exit(bool(failures))
