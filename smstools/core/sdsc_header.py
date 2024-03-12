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
    DATE = 2
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
        return 'TODO: sdsc value'

    @property
    def version(self):
        return 'TODO: version value'

    @property
    def date(self):
        return 'TODO: date value'

    @property
    def author_pointer(self):
        return 'TODO: author pointer value'

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
