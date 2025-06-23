print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.test_settings")
from main.settings.settings import *
MEDIA_ROOT = str(DATA_ROOT / "test_media")

DEBUG = False
LOG_LEVEL = "DEBUG"
LOG_ROOT = "/tmp/"
LOG_FILENAME = "test.log"

TRACE_SETTINGS_ENABLED = True

