from typing import LiteralString

from ..config.config import Config


class Message:
    _client: str
    _uc: int

    def __init__(self, client: str, uc: int) -> None:
        self._client = client
        self._uc = uc
    
    def __str__(self) -> str:
        return f"Cliente(Nome: {self._client}, Unidade Consumidora: {self._uc})"
    
    def getMessage(self) -> str:
        return Config.MESSAGE.format(cliente = self._client, unidade_consumidora = self._uc)
        