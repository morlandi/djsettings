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
