from enum import Enum

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


class SdscHeader:

    def __init__(self, rom_data):
        self._rom_data = rom_data

    def __str__(self):
        if not self.sdsc:
            return 'not available'

        return f'''\
SDSC HEADER:\n
sdsc:\t\t\t{self.sdsc}
version:\t\t{self.version}
date:\t\t\t{self.date}
author pointer:\t\t{self.author_pointer}
author:\t\t\t{self.author}
name pointer:\t\t{self.name_pointer}
name:\t\t\t{self.name}
description pointer:\t{self.description_pointer}
description:\t\t{self.description}
        '''

    @property
    def sdsc(self):
        value = self._rom_data[Offsets.SDSC.value:Offsets.SDSC.value \
            + Lengths.SDSC.value]

        return value.decode()

    @property
    def version(self):
        value = self._rom_data[Offsets.VERSION.value:Offsets.VERSION.value \
            + Lengths.VERSION.value]

        return value.hex()

    @property
    def date(self):
        value = self._rom_data[Offsets.DATE.value:Offsets.DATE.value \
            + Lengths.DATE.value]

        day = hex(value[0]).strip('x')[2:]
        mounth = hex(value[1]).strip('x')[2:]
        year = hex(value[3]).strip('x')[2:] + hex(value[2]).strip('x')[2:]

        return f'{day}/{mounth}/{year}'

    @property
    def author_pointer(self):
        value = self._rom_data[Offsets.AUTHOR_POINTER.value:Offsets.AUTHOR_POINTER.value \
            + Lengths.AUTHOR_POINTER.value]

        return '0x' + str(value.hex()[2:4]) + str(value.hex()[0:2])

    @property
    def author(self):
        return 'TODO: author value'

    @property
    def name_pointer(self):
        return 'TODO: name pointer value'

    @property
    def name(self):
        return 'TODO: name value'

    @property
    def description_pointer(self):
        return 'TODO: description pointer value'

    @property
    def description(self):
        return 'TODO: description value'
