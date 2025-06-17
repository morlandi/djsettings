print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.local")
from main.settings.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*', ]

LOG_LEVEL = "DEBUG"
TRACE_SETTINGS_ENABLED = True

# discard email messages
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
