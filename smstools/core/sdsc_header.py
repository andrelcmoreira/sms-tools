from enum import Enum
from struct import unpack

from core.header import Header

# https://www.smspower.org/Development/SDSCHeader

class Offsets(Enum):
    SDSC = 0x7fe0
    VERSION = 0x7fe4
    DATE = 0x7fe6
    AUTHOR_POINTER = 0x7fea
    NAME_POINTER = 0x7fec
    DESCRIPTION_POINTER = 0x7fee


class Lengths(Enum):
    SDSC = 4
    VERSION = 2
    DATE = 4
    AUTHOR_POINTER = 2
    NAME_POINTER = 2
    DESCRIPTION_POINTER = 2


class SdscHeader(Header):

    def __init__(self, rom_data):
        Header.__init__(self, rom_data)

    def __str__(self):
        if not self.sdsc:
            return 'not available'

        return (
            'SDSC HEADER\n\n'
            f'sdsc:\t\t\t{self.sdsc}\n'
            f'version:\t\t{self.version}\n'
            f'date:\t\t\t{self.date}\n'
            f'author pointer:\t\t{self.author_pointer}\n'
            f'author:\t\t\t{self.author}\n'
            f'name pointer:\t\t{self.name_pointer}\n'
            f'name:\t\t\t{self.name}\n'
            f'description pointer:\t{self.description_pointer}\n'
            f'description:\t\t{self.description}'
        )

    @property
    def sdsc(self):
        value = self.get_field(Offsets.SDSC.value, Lengths.SDSC.value)

        return value.decode()

    @property
    def version(self):
        value = self.get_field(Offsets.VERSION.value, Lengths.VERSION.value)

        return value.hex()

    @property
    def date(self):
        value = self.get_field(Offsets.DATE.value, Lengths.DATE.value)

        return f'{value[1]:x}/{value[0]:x}/{value[3]:x}{value[2]:x}'

    @property
    def author_pointer(self):
        value = self.get_field(Offsets.AUTHOR_POINTER.value,
                               Lengths.AUTHOR_POINTER.value)

        return hex(unpack('<H', value)[0])

    @property
    def author(self):
        author_addr = int(self.author_pointer, 16)

        return self.get_ptr_field(author_addr)

    @property
    def name_pointer(self):
        value = self.get_field(Offsets.NAME_POINTER.value,
                               Lengths.NAME_POINTER.value)

        return hex(unpack('<H', value)[0])

    @property
    def name(self):
        name_addr = int(self.name_pointer, 16)

        return self.get_ptr_field(name_addr)

    @property
    def description_pointer(self):
        value = self.get_field(Offsets.DESCRIPTION_POINTER.value,
                               Lengths.DESCRIPTION_POINTER.value)

        return hex(unpack('<H', value)[0])

    @property
    def description(self):
        description_addr = int(self.description_pointer, 16)

        return self.get_ptr_field(description_addr)
