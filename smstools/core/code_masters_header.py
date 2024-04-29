# based on https://www.smspower.org/Development/CodemastersHeader
from enum import Enum
from struct import unpack

from core.header import Header
from core.sdsc_header import SdscHeader


class Offsets(Enum):
    BANKS_NUMBER = 0x7fe0
    DAY = 0x7fe1
    MONTH = 0x7fe2
    YEAR = 0x7fe3
    HOUR = 0x7fe4
    MINUTE = 0x7fe5
    CHECKSUM = 0x7fe6
    CHECKSUM_WORD = 0x7fe8 # TODO: give a meaningful name for this field


class Lengths(Enum):
    BANKS_NUMBER = 1
    DAY = 1
    MONTH = 1
    YEAR = 1
    HOUR = 1
    MINUTE = 1
    CHECKSUM = 2
    CHECKSUM_WORD = 2


class CodeMastersHeader(Header):

    def __init__(self, rom_data):
        Header.__init__(self, rom_data)

        self._sdsc = SdscHeader(rom_data)

    def header_exists(self):
        return (not self._sdsc.header_exists()) and \
                (not self.banks_number in ('0', '255'))

    def __str__(self):
        if not self.header_exists():
            return 'CODEMASTERS HEADER\n\nnot available'

        return (
            'CODEMASTERS HEADER\n\n'
            f'number of banks:\t{self.banks_number}\n'
            f'timestamp:\t\t{self.hour}:{self.minute} '
            f'{self.day}/{self.month}/{self.year} (hh:mm dd/mm/yy)\n'
            f'checksum:\t\t{self.checksum}\n'
            f'checksum word:\t\t{self.checksum_word}\n'
        )

    @property
    def banks_number(self):
        number = self.get_field(Offsets.BANKS_NUMBER.value,
                                Lengths.BANKS_NUMBER.value)

        return f'{number[0]:d}'

    @property
    def day(self):
        day = self.get_field(Offsets.DAY.value,
                             Lengths.DAY.value)

        return f'{day[0]:02x}'

    @property
    def month(self):
        month = self.get_field(Offsets.MONTH.value,
                               Lengths.MONTH.value)

        return f'{month[0]:02x}'

    @property
    def year(self):
        year = self.get_field(Offsets.YEAR.value,
                              Lengths.YEAR.value)

        return f'{year[0]:x}'

    @property
    def hour(self):
        hour = self.get_field(Offsets.HOUR.value,
                              Lengths.HOUR.value)

        return f'{hour[0]:02x}'

    @property
    def minute(self):
        minute = self.get_field(Offsets.MINUTE.value,
                                Lengths.MINUTE.value)

        return f'{minute[0]:02x}'

    @property
    def checksum(self):
        checksum = self.get_field(Offsets.CHECKSUM.value,
                                  Lengths.CHECKSUM.value)

        return hex(unpack('<H', checksum)[0])

    @property
    def checksum_word(self):
        checksum = self.get_field(Offsets.CHECKSUM_WORD.value,
                                  Lengths.CHECKSUM_WORD.value)

        return hex(unpack('<H', checksum)[0])
