# based on https://www.smspower.org/Development/ROMHeader
from enum import Enum

from core.header import Header

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
        if not self.header_exists():
            return 'ROM HEADER\n\nnot available'

        return (
            'ROM HEADER\n\n'
            f'tmr sega:\t{self.tmr_sega}\n'
            f'ckecksum:\t{self.checksum}\n'
            f'product code:\t{self.product_code}\n'
            f'version:\t{self.version}\n'
            f'region code:\t{self.region_code}\n'
            f'rom size:\t{self.rom_size}'
        )

    def header_exists(self):
        return len(self.tmr_sega) > 0

    @property
    def tmr_sega(self):
        tmr_sega = self.get_field(Offsets.TMR_SEGA.value,
                                  Lengths.TMR_SEGA.value)

        return tmr_sega.decode()

    @property
    def checksum(self):
        cksum = self.get_field(Offsets.CHECKSUM.value, Lengths.CHECKSUM.value)

        return f'0x{cksum.hex()}'

    @property
    def product_code(self):
        prod_code = self.get_field(Offsets.PRODUCT_CODE.value,
                                   Lengths.PRODUCT_CODE.value)

        return f'0x{prod_code.hex()[0:5]}'

    @property
    def version(self):
        value = self.get_field(Offsets.VERSION.value, Lengths.VERSION.value)
        version = value.hex()[1]

        return f'0x{version}'

    @property
    def region_code(self):
        value = self.get_field(Offsets.REGION_CODE.value,
                               Lengths.REGION_CODE.value)
        region_code = int(value.hex()[0], 16)
        region_code_str = RegionCode(region_code) \
            .name \
            .replace('_', ' ') \
            .lower()

        return f'0x{region_code:x} ({region_code_str})'

    @property
    def rom_size(self):
        value = self.get_field(Offsets.ROM_SIZE.value,
                               Lengths.ROM_SIZE.value)
        rom_size = int(value.hex()[1], 16)
        rom_size_str = RomSize(rom_size) \
            .name \
            .split('_')[1] \
            .lower()

        return f'0x{rom_size:x} ({rom_size_str})'
