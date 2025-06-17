print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.local")
from main.settings.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*', ]

LOG_LEVEL = "DEBUG"
TRACE_SETTINGS_ENABLED = True

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": PROJECT_INSTANCE,
#         "USER": PROJECT_INSTANCE,
#         "PASSWORD": "*****************************", # See deployment
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }

# discard email messages
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
