#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.test.utils import get_runner

# See "Using the Django test runner to test reusable applications":
# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications

APP_LIST = [
    "myapp",
]

def remove_db():
    # Apply only when using Postgresql:
    if 'psycopg' in connection.settings_dict['ENGINE']:
        testdb_name = "test_" + connection.settings_dict["NAME"]
        command = "psql -c 'drop database if exists \"%s\";'" % testdb_name
        rc = os.system(command)

def parse_app(option):
    """
    Try to transform "test_run_task_once_formula_file1 (tasks.tests.test_import_data.ImportDataTestCase)"
    as "tasks.tests.test_import_data.ImportDataTestCase.test_run_task_once_formula_file1"
    """
    app = option
    pos_open_brace = option.find("(")
    if pos_open_brace >= 0:
        pos_close_brace = option.find(")", pos_open_brace)
        right = option[:pos_open_brace]
        left = option[pos_open_brace + 1 : pos_close_brace]
        app = left.strip() + "." + right.strip()
    return app


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--verbosity", "-v", type=int, default=2)
    parser.add_argument(
        "--app",
        "-a",
        type=str,
        default="",
        help="App filter; available values: %s" % str(APP_LIST),
    )
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
    parser.add_argument(
        "--sqlite",
        "-s",
        action="store_true",
        help="Use sqlite (in memory) instead of PostgreSQL)",
    )
    parser.add_argument(
        "--apply-lint",
        "-l",
        action="store_true",
    )
    args = parser.parse_args()

    verbosity = args.verbosity
    os.environ["DJANGO_TEST_RUNNER_VERBOSITY"] = str(verbosity)

    if args.app:
        # assert args.app in APP_LIST, ('"%s" not available; valid apps are: %s' % (args.app, str(APP_LIST)))
        app_list = [
            parse_app(args.app),
        ]
    else:
        app_list = APP_LIST

    keepdb = True
    if args.no_keepdb:
        keepdb = False

    os.environ["DJANGO_SETTINGS_MODULE"] = (
        "main.settings.test_settings_no_migrations"
        if args.no_migrations
        else "main.settings.test_settings"
    )

    if args.sqlite:
        print("Override DATABASES settings with sqlite ...")
        settings.DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                #'NAME': os.path.join(BASE_DIR, 'testdb.sqlite3'),
                "NAME": ":memory:",
            }
        }

    django.setup()

    if not args.sqlite:
        remove_db()

    if args.apply_lint:
        print("\x1b[1;37;44m lint started... \x1b[0m")
        os.system("./lint .")
        print("\x1b[1;37;44m lint completed. \x1b[0m")

    # # Set log level based on verbosity
    # levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO]
    # loglevel = levels[min(len(levels) - 1, verbosity)]  # capped to number of levels
    # logging.disable(loglevel)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, keepdb=keepdb)
    failures = test_runner.run_tests(app_list)
    sys.exit(bool(failures))
