import logging
from os.path import isfile, basename
from time import sleep
from pandas import DataFrame, read_csv, read_excel, read_table
from typing import Iterable
from ..config.messages import ErrorsMessages, LoggingMessages
from ..utils.exceptions.dataExceptions import DataException

class Data:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._df: DataFrame
        self._exclusionList: list = [0, 83900000000, 83999999999]
        self._path = None

    def _validateColumns(self, columns: Iterable["str"]) -> bool:
        essentials = (
            "UC", "NOME", "NUMTEL", "NUMTEL2"
            )
        return not any(essential not in columns for essential in essentials)
    
    def _fill(self, df: DataFrame):
        df = df.dropna(how='all')
        df[["NUMTEL", "NUMTEL2"]] = df[["NUMTEL", "NUMTEL2"]].fillna(0)
        df[["NUMTEL", "NUMTEL2"]] = df[["NUMTEL", "NUMTEL2"]].astype(int)
        df = df.loc[(~df["NUMTEL2"].isin(self._exclusionList)) | (~df["NUMTEL"].isin(self._exclusionList))]
        return df
    
    def _updateStatus(self, status: str, num_cdc: int | None = None):
        if num_cdc is None:
            self._df['Status'] = status
        else:
            self._df.loc[self._df.UC == num_cdc, 'Status'] = status
        self._df.to_excel('temp/~temp_file.xlsx', index=False)

    def setDelivered(self, num_cdc: int) -> None:
        """Atualiza o status do cdc para entregue."""
        self._updateStatus('Entregue', num_cdc)

    def setNotFound(self, num_cdc: int) -> None:
        """Atualiza o status do cdc para não encontrado."""
        self._updateStatus('Não encontrado', num_cdc)

    def save(self) -> None:
        """Salva o DataFrame em um arquivo Excel."""
        temp_df = read_excel(self._path)
        for _, item in self._df.iterrows():
            temp_df.loc[temp_df.UC == item.UC, 'Status'] = item.Status
        temp_df.to_excel(self._path, index=False)

    def read_file(self, path:str|None):
        if path is None or not isfile(path):
            raise DataException(ErrorsMessages.INVALID_PATH_ERR.format(path=path))
        extension = path.split('.')[-1].lower()
        try:
            match(extension):
                case 'xlsx' | 'xls':
                    temp_df = read_excel(path)
                case 'csv':
                    temp_df = read_csv(path, sep=";")
                case 'txt':
                    temp_df = read_table(path)
                case _:
                    raise DataException(ErrorsMessages.EXTENSION_NOT_SUPPORTED)        
        except PermissionError:
                self.logger.warning(LoggingMessages.FILE_BUSY.format(file = basename(path)))
                sleep(30)
                return self.read_file(path)
        if self._validateColumns(temp_df.columns):
            self._df = self._fill(temp_df)
            self._path = path
        else:
            raise DataException(ErrorsMessages.NO_COLUMNS_IN_DATA)

    @property
    def getData(self) -> DataFrame:
        return self._df
    
