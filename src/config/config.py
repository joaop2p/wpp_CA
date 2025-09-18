from ..config import data_path, driver_cache, config

class Config:
    VERSION = "0.0.5"
    REPOSITORY_PDF = ""
    REPOSITORY_JGP = ""
    GENERIC_ERROR_CODE = 1
    SUCCESS_CODE = 0
    DATA_FILE = data_path
    LOG_PATH = config['SETTINGS']['log_path']
    CACHE_DRIVER_PATH = driver_cache
    MESSAGE = config['MESSAGE']['text']
    IMAGE_PATH = config['MESSAGE']['image_path']
    HEADLESS_MODE = config.getboolean('SETTINGS', 'headless', fallback=True)

    
