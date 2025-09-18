from ..model.contact import Contact
from ..model.message import Message


class Client:
    _contact: Contact
    _message: Message
    _uc: int
    
    def __init__(self, message: Message, contact: Contact, uc: int) -> None:
        self._contact = contact
        self._message = message
        self._uc = uc

    @property
    def getUC(self) -> int:
        """Retorna o número do UC (Unidade Consumidora) do cliente."""
        return self._uc

    @property
    def getContact(self) -> Contact:
        return self._contact

    @property
    def getMessage(self) -> Message:
        return self._message

    @property
    def ready(self) -> bool:
        for attr in vars(self):
            if getattr(self, attr) is None:
                return False
        return True 