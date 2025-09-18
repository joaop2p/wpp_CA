import logging
from os import getlogin
import sys
from src.config.messages import LoggingMessages
from src.config.config import Config
from src.config.log import Log
from src.launcher import Launcher

class Nome_Generico(Log):
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(
            LoggingMessages.WELCOME.format(
                version = Config.VERSION, login = getlogin()
                ))
    
    def main(self) -> None:
        launcher = Launcher(False)
        code = Config.SUCCESS_CODE
        try:
            launcher.wppProcess(Config.DATA_FILE)
        except Exception as e:
            self.logger.critical(e)
            code = Config.GENERIC_ERROR_CODE
        finally:
            self.logger.info(LoggingMessages.EXIT.format(code=code))
            sys.exit(code)

if __name__ == "__main__":
    Nome_Generico().main()
