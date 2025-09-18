class Contact:
    _num1: int
    _num2: int

    def __init__(self, num1: int, num2: int) -> None:
        self._num1 = num1
        self._num2 = num2

    def getNum1(self) -> int:
        return self._num1

    def getNum2(self) -> int | None:
        if self._num2 != self._num1:
            return self._num2