print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.debug")
from main.settings.local import *

DEBUG = True
ALLOWED_HOSTS = [
    "*",
]

QUERYCOUNT = {
    "IGNORE_ALL_REQUESTS": False,
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 0,
    },
    "DISPLAY_ALL": True,
    "DISPLAY_PRETTIFIED": True,
    "COLOR_FORMATTER_STYLE": "monokai",
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
    "DISPLAY_DUPLICATES": 0,
}

#
# LOGGING
#

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         # 'file': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.FileHandler',
#         #     'filename': '/home/comatrol1/logs/django.log',
#         # },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#         },
#     },
#     'loggers': {
#         'sorl.thumbnail': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.db.backends': {
#             'handlers': ['console', ],
#             'level': 'DEBUG',
#         },
#     },
# }

