import logging
from random import randint
from time import sleep
import traceback
from typing import Literal

from .config.config import Config
from .data.data import Data
from .model.message import Message
from .config.messages import LoggingMessages
from .actions import Actions
from pandas import DataFrame
from typing import Iterable
from .model.message import Message
from .model.client import Client
from .model.contact import Contact

class Launcher(Data):
    def __init__(self, debug_app: bool = True) -> None:
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

    def capitalizeName(self, name: str) -> str:
        return ' '.join([sub.capitalize() for sub in name.split(" ")])

    def buildClients(self, df: DataFrame) -> Iterable[Client]:
        clients: Iterable[Client] = []
        for _, row in df.iterrows():
            new_contact = Contact(row.NUMTEL, row.NUMTEL2)
            new_message = Message(client=row.NOME, uc=row.UC)
            client = Client(contact=new_contact, message=new_message, uc=row.UC)
            if client.ready:
                clients.append(client)
        return clients

    def start_chat(self, number: int | None) -> int | None:
        if number is None or number in self._exclusionList:
            return 
        if number == 0 or not self.actions.search(number):
            self._exclusionList.append(number)
            return
        return number

    def default_send_messages(self, client: Client):
        number_used = self.start_chat(client.getContact.getNum1())
        if number_used is None:
            number_used = self.start_chat(client.getContact.getNum2())
            if number_used is None:
                return False, number_used
        self.actions.send_message(client.getMessage.getMessage(), True)
        self.actions.send_file(Config.IMAGE_PATH, mode='video')
        self.actions.exit_chat()
        return True, number_used

    def wppProcess(self, base_path: str | None) -> None:
        self.read_file(base_path)
        clients = self.buildClients(self.getData)
        # print(clients[0].getMessage.getMessage().replace(";", '\n'))
        # exit(1)
        if clients:
            self.actions = Actions()
            self.actions.start_whatsapp()
            try:
                for client in clients:
                    logging.info(LoggingMessages.CURRENT_CLIENT.format(uc = client.getUC))
                    result, number_used = self.default_send_messages(client)
                    if result:
                        self.logger.info(LoggingMessages.MESSAGE_SENDED.format(number=number_used))
                        self.setDelivered(client.getUC)
                    else:
                        self.logger.warning(LoggingMessages.NUMBER_NOT_FIND.format(number=number_used))
                        self.setNotFound(client.getUC)
                    sleep(randint(4, 7))
            except KeyboardInterrupt:
                self.logger.warning(f"Operação interrompida pelo usuário.")
            except Exception as e:
                self.logger.critical("Exceção detectada:\n%s", ''.join(traceback.format_exception(type(e), e, e.__traceback__)))
            finally:
                sleep(20)
                self.save()
        sleep(3)
