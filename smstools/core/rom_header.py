from enum import Enum

from core.header import Header

# https://www.smspower.org/Development/ROMHeader

# TODO: consider the 1ff0 and 3ff0 offsets as alternative offsets to TMR_SEGA
class Offsets(Enum):
    TMR_SEGA = 0x7ff0
    RESERVED_SPACE = 0x7ff8
    CHECKSUM = 0x7ffa
    PRODUCT_CODE = 0x7ffc
    VERSION = 0x7ffe
    REGION_CODE = 0x7fff
    ROM_SIZE = 0x7fff


class RomSize(Enum):
    SIZE_8KB = 0xa
    SIZE_16KB = 0xb
    SIZE_32KB = 0xc
    SIZE_48KB = 0xd
    SIZE_64KB = 0xe
    SIZE_128KB = 0xf
    SIZE_256KB = 0x0
    SIZE_512KB = 0x1
    SIZE_1MB = 0x2


class RegionCode(Enum):
    SMS_JAPAN = 3
    SMS_EXPORT = 4
    GG_JAPAN = 5
    GG_EXPORT = 6
    GG_INTERNATIONAL = 7


class Lengths(Enum):
    TMR_SEGA = 8
    RESERVED_SPACE = 2
    CHECKSUM = 2
    PRODUCT_CODE = 3 # 2 bytes + 1 nibble
    VERSION = 1 # 1 nibble
    REGION_CODE = 1 # 1 nibble
    ROM_SIZE = 1 # 1 nibble


class RomHeader(Header):

    def __init__(self, rom_data):
        Header.__init__(self, rom_data)

    def __str__(self):
        if not self.tmr_sega:
            return 'not available'

        return (
            'ROM HEADER\n\n'
            f'tmr sega:\t{self.tmr_sega}\n'
            f'ckecksum:\t{self.checksum}\n'
            f'product code:\t{self.product_code}\n'
            f'version:\t{self.version}\n'
            f'region code:\t{self.region_code}\n'
            f'rom size:\t{self.rom_size}'
        )

    @property
    def tmr_sega(self):
        value = self.get_field(Offsets.TMR_SEGA.value, Lengths.TMR_SEGA.value)

        return value.decode()

    @property
    def checksum(self):
        pass

    @property
    def product_code(self):
        pass

    @property
    def version(self):
        pass

    @property
    def region_code(self):
        pass

    @property
    def rom_size(self):
        pass
