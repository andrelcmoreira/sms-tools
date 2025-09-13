# based on https://www.smspower.org/Development/SDSCHeader
from enum import Enum
from struct import unpack

from core.header import Header


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

    def header_exists(self) -> bool:
        return self.sdsc == 'SDSC'

    def __str__(self) -> str:
        if not self.header_exists():
            return f'SDSC HEADER\n\n{self._NOT_AVAILABLE_INFO}'

        return (
            'SDSC HEADER\n\n'
            f'sdsc:\t\t\t{self.sdsc}\n'
            f'version:\t\t{self.version}\n'
            f'date:\t\t\t{self.date} (dd/mm/yy)\n'
            f'author pointer:\t\t{self.author_pointer}\n'
            f'author:\t\t\t{self.author}\n'
            f'name pointer:\t\t{self.name_pointer}\n'
            f'name:\t\t\t{self.name}\n'
            f'description pointer:\t{self.description_pointer}\n'
            f'description:\t\t{self.description}'
        )

    @property
    def sdsc(self) -> str:
        try:
            sdsc = self.get_field(Offsets.SDSC.value,
                                  Lengths.SDSC.value)
            if sdsc in (b'\xff\xff\xff\xff', b'\x00\x00\x00\x00'):
                return ''

            return sdsc.decode()
        except UnicodeDecodeError:
            return ''

    @property
    def version(self) -> str:
        version = self.get_field(Offsets.VERSION.value,
                                 Lengths.VERSION.value)

        return f'{version[0]:x}.{version[1]:02x}'

    @property
    def date(self) -> str:
        date = self.get_field(Offsets.DATE.value,
                              Lengths.DATE.value)

        return f'{date[0]:02x}/{date[1]:02x}/{date[3]:x}{date[2]:x}'

    @property
    def author_pointer(self) -> str:
        author_ptr = self.get_field(Offsets.AUTHOR_POINTER.value,
                                    Lengths.AUTHOR_POINTER.value)

        return hex(unpack('<H', author_ptr)[0])

    @property
    def author(self) -> str:
        author_addr = int(self.author_pointer, 16)

        return self.get_str_field(author_addr)

    @property
    def name_pointer(self) -> str:
        name_ptr = self.get_field(Offsets.NAME_POINTER.value,
                                  Lengths.NAME_POINTER.value)

        return hex(unpack('<H', name_ptr)[0])

    @property
    def name(self) -> str:
        name_addr = int(self.name_pointer, 16)

        return self.get_str_field(name_addr)

    @property
    def description_pointer(self) -> str:
        desc_ptr = self.get_field(Offsets.DESCRIPTION_POINTER.value,
                                  Lengths.DESCRIPTION_POINTER.value)

        return hex(unpack('<H', desc_ptr)[0])

    @property
    def description(self) -> str:
        desc_addr = int(self.description_pointer, 16)

        return self.get_str_field(desc_addr)
