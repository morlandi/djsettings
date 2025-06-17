import inspect
import json
import os
import time
import traceback

import IPython
from django.conf import settings

try:
    import rich
except ModuleNotFoundError:
    rich = None


def trace_line(message):
    if not rich:
        print("\x1b[1;37;44m %s \x1b[1;39;49m" % str(message))
    else:
        rich.get_console().print(" [white on dark_blue]%s " % message)


def trace_func(fn):
    """
    Sample usage:

        class MyClass(object):
            ...

            @trace_func
            def my_func(self, user, obj):
                ...
    """

    def trace_params(funcname, title, subtitle, params, retvalue):
        if not rich:
            trace_line(title)
            for param in params:
                trace_line("%s: %s" % (param[0], param[1]))
            trace_line("retvalue: %s" % retvalue)
            trace_line(subtitle)
        else:
            tokens = title.split(funcname)
            if len(tokens) == 2:
                title = "[white]%s[bold yellow]%s[white]%s" % (
                    tokens[0],
                    funcname,
                    tokens[1],
                )

            table = rich.table.Table(
                show_edge=False,
                show_header=True,
                expand=False,
                box=rich.box.SIMPLE,
            )
            table.add_column("Param", justify="left", style="cyan", no_wrap=True)
            table.add_column("Value", justify="left", style="yellow", no_wrap=True)
            for row in params:
                table.add_row(row[0], str(row[1]))
            table.add_row("[white]Return value", "[white]%s" % retvalue)
            panel = rich.panel.Panel(
                table,
                title="[white]" + title,
                subtitle=subtitle,
                highlight=True,
                border_style="bright_blue",
                box=rich.box.DOUBLE,
            )
            rich.get_console().print(panel)

    def func_wrapper(*args, **kwargs):
        if not settings.CCMS_DEBUG_TRACE_ENABLED:
            return fn(*args, **kwargs)

        trace_line(">>> %s()" % fn.__name__)

        # Call func and calculate elapsed time
        t0 = time.time()
        retvalue = fn(*args, **kwargs)
        t1 = time.time()

        ms = ".%03d" % int((t1 - t0) * 1000)
        elapsed = time.strftime("%H:%M:%S", time.gmtime(t1 - t0)) + ms

        # Prepare title and subtitle
        title = (
            str(fn)
            if (inspect.isclass(fn) or callable(fn) or inspect.ismodule(fn))
            else str(type(fn))
        )
        subtitle = "Elapsed: " + elapsed

        # Retrieve parameter/value pairs
        params = []
        i = 0
        for key, fparam in inspect.signature(fn).parameters.items():
            value = args[i] if i < len(args) else fparam.default
            if key in kwargs:
                value = kwargs[key]
            i += 1
            params.append((key, value))

        trace_params(fn.__name__, title, subtitle, params, retvalue)
        trace_line("<<< %s() - %s" % (fn.__name__, elapsed))

        return retvalue

    return func_wrapper


def trace_items(items, title="", subtitle=""):
    from rich.panel import Panel
    from rich.table import Table

    table = Table(
        show_edge=False,
        show_header=True,
        expand=False,
        box=rich.box.SIMPLE,
    )
    table.add_column("Name", justify="left", style="cyan", no_wrap=False)
    table.add_column("Value", justify="left", style="yellow", no_wrap=False)
    for name, value in items.items():
        table.add_row(name, str(value))
        panel = rich.panel.Panel(
            table,
            # title="[white] " + title,
            title=title,
            subtitle=subtitle,
            highlight=False,
            border_style="bright_blue",
            box=rich.box.DOUBLE,
        )
    rich.get_console().print(panel)


def trace_settings():

    if os.environ.get("RUN_MAIN") is not None:
        return

    if not settings.TRACE_SETTINGS_ENABLED:
        return

    try:
        # Questa cosa infastidisce "runtests.py" e pertanto intercettiamo eventuali exceptions
        names = [
            "DEBUG",
            # "HTTP_PROTOCOL",
            # "HOSTNAME",
            'ALLOWED_HOSTS',
            "STATIC_URL",
            "MEDIA_URL",
            "MEDIA_URL",
            "STATIC_ROOT",
            "MEDIA_ROOT",
            "LOG_ROOT",
            "LOG_FILENAME",
            "LOG_LEVEL",
            # "CACHE_URL",
            # "REDIS_URL",
            # "UNIDRV_REDIS_URL",
            # "PROJECT_NAME",
            # "PROJECT_INSTANCE",
            # # "CORS_ALLOWED_ORIGINS",
            "SESSION_COOKIE_NAME",
            "CSRF_TRUSTED_ORIGINS",
            "CSRF_COOKIE_DOMAIN",
        ]


        items = {k: getattr(settings, k) for k in names}
        db = getattr(settings, "DATABASES")["default"]
        items.update({
            "DATABASE_ENGINE": db['ENGINE'],
            "DATABASE_NAME": db['NAME'],
        })

        # db = settings.get("DATABASES")["default"]
        # items.update(
        #     {"DATABASE": f"postgresql://{db['USER']}:*******@{db['HOST']}/{db['NAME']}"}
        # )

        trace_items(items, title="Settings", subtitle="")

    except Exception as e:
        print("ERROR: " + str(e))
        print(traceback.format_exc())

################################################################################

if __name__ == "__main__":

    @trace_func
    def my_func(text):
        logger.info("inside function ...")
        return 1

    class MyClass(object):
        @trace_func
        def my_method(self, user):
            logger.info("inside my_method ...")
            return 1

    def blabla():
        for i in range(3):
            print("bla bla")

    import logging

    #  before module import which use logging.basicConfig
    logging.basicConfig(format="%(asctime)s - %(levelname)s- %(message)s")
    logger = logging.getLogger(__name__)

    blabla()
    my_func("test me")
    blabla()
    obj = MyClass()
    obj.my_method("me")
    blabla()
