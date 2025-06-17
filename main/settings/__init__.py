import os

settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "")

if not settings_module:
    raise RuntimeError("DJANGO_SETTINGS_MODULE is not set!")

# Skip importing local.py if running tests with test settings
if settings_module.startswith("main.settings.test_setting"):
    # Let Django use the test settings module directly
    pass
else:
    try:
        from main.settings.local import *
    except ModuleNotFoundError:
        from main.settings.settings import *

# Poor man debugging when DEBUG=False
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from main.settings.extra_settings import *
except ModuleNotFoundError:
    pass


