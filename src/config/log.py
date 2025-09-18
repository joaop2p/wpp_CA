import logging
from os import mkdir
from os.path import isdir, join

from .config import Config

class Log:
    if not isdir(Config.LOG_PATH):
        mkdir(Config.LOG_PATH)
    app_handler = logging.FileHandler(join(Config.LOG_PATH, "app.log"))
    app_handler.setLevel(logging.INFO)
    error_handler = logging.FileHandler(join(Config.LOG_PATH, "error.log"))
    error_handler.setLevel(logging.ERROR)
    logging.basicConfig(
        level=logging.INFO,
        encoding="utf-8",
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            app_handler,
            error_handler,
            logging.StreamHandler()
        ]
    )