print("\x1b[1;37;44m %s \x1b[1;39;49m" % "import main.settings.test_settings")
from main.settings.settings import *
MEDIA_ROOT = DATA_ROOT / "test_media"

DEBUG = False
LOG_LEVEL = "DEBUG"
LOG_ROOT = "/tmp/"
LOG_FILENAME = "test.log"

# from .logging import get_logging_config
# LOGGING = get_logging_config(
#     verbose=True,
#     log_level=LOG_LEVEL,
#     log_root=LOG_ROOT,
#     log_filename=LOG_FILENAME)
