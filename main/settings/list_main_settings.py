from django.conf import settings


def list_main_settings():
    """
    List main settings for debug purposes and documentation
    """

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
        "LOG_TO_CONSOLE",
        "LOG_ROOT",
        "LOG_FILENAME",
        "LOG_LEVEL",
        # "CACHE_URL",
        # "REDIS_URL",
        # "UNIDRV_REDIS_URL",
        "PROJECT_NAME",
        "PROJECT_INSTANCE",
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

    return items
