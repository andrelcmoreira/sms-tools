from abc import abstractmethod, ABC


class Header(ABC):

    def __init__(self, rom_data: bytes):
        self._rom_data = rom_data

    @abstractmethod
    def header_exists(self) -> bool:
        pass

    def get_field(self, offset: int, length: int) -> bytes:
        value = self._rom_data[offset:offset + length]

        return value

    def get_str_field(self, offset: int) -> str:
        field = ''

        for byte in self._rom_data[offset:]:
            if not byte: # end of string
                break

            field += chr(byte)

        return field
