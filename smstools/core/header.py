from abc import abstractmethod, ABC

class Header(ABC):

    def __init__(self, rom_data):
        self._rom_data = rom_data

    @abstractmethod
    def header_exists(self):
        pass

    def get_field(self, offset, length):
        value = self._rom_data[offset:offset + length]

        return value

    def get_str_field(self, offset):
        field = []

        for byte in self._rom_data[offset:]:
            if not byte:
                break

            field.append(chr(byte))

        return ''.join(field)
