from abc import ABC, abstractmethod
from argparse import ArgumentParser
from colorama import Fore
from dataclasses import dataclass
from enum import Enum
from sys import argv


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


@dataclass
class Field:
    name: str
    offset: Offsets
    size: Lengths


class FieldValidator(ABC):

    def __init__(self, field):
        self._field = field

    @abstractmethod
    def check(self, data, rom_buffer):
        pass

    @staticmethod
    def show_result(func):
        def wrapper(self, rom_buffer):
            start_offs = self._field.offset.value
            end_offs = start_offs + self._field.size.value

            try:
                data = rom_buffer[start_offs:end_offs]
                func(self, data, rom_buffer)

                print('[' + Fore.GREEN + '  OK  ' + Fore.RESET + '] '
                      + self._field.name)
            except AssertionError as e:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self._field.name + '...' + str(e))
            except UnicodeDecodeError:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self._field.name)

        return wrapper


class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('TMR SEGA', Offsets.TMR_SEGA,
                                            Lengths.TMR_SEGA))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = b'TMR SEGA'

        assert data == expected, f'{data.decode()} != {expected.decode()}'


class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Reserved space',
                                            Offsets.RESERVED_SPACE,
                                            Lengths.RESERVED_SPACE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = [b'\x00\x00', b'\xff\xff', b'\x20\x20']

        assert (data == expected[0]) or (data == expected[1]) \
                or (data == expected[2]), \
                "the reserved space must be '0x0000', '0xffff' or '0x2020'"


class RomChecksumCalc:

    _PAGE_SIZE = 0x4000

    @classmethod
    def calculate(cls, rom):
        # first page address after the rom header
        start_range = 0x8000
        # number of pages after header
        rem_pages = int(RomSizeCalc.get_virtual_size(rom) / cls._PAGE_SIZE) - 2
        # checksum of first two pages
        cksum = cls._checksum(rom, 0, 0, Offsets.TMR_SEGA.value)

        for _ in range(0, rem_pages):
            cksum = cls._checksum(rom, cksum, start_range, cls._PAGE_SIZE)
            start_range += cls._PAGE_SIZE

        return cksum.to_bytes(Lengths.CHECKSUM.value, byteorder='little')

    @classmethod
    def _checksum(cls, buffer, last_cksum, start_range, offset):
        cs1 = (last_cksum >> 8) & 0xff
        cs2 = last_cksum & 0xff
        cs3 = e = ov1 = ov2 = 0

        for i in range(start_range, start_range + offset):
            e = cs2
            ov1 = e
            e += buffer[i]
            ov2 = e & 0xff

            if ov1 > ov2:
                cs3 = 1

            cs2 = e & 0xff
            e = cs1 + cs3
            cs3 = 0
            cs1 = e

        last_cksum = (cs1 << 8) & 0xff00 | cs2

        return last_cksum & 0xffff


class ChecksumValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Checksum', Offsets.CHECKSUM,
                                            Lengths.CHECKSUM))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        checksum = RomChecksumCalc.calculate(rom_buffer)

        assert data == checksum, f'0x{data.hex()} != 0x{checksum.hex()}'


class ProductCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Product code',
                                            Offsets.PRODUCT_CODE,
                                            Lengths.PRODUCT_CODE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        code = data.hex()[0:5]

        assert code.isdigit(), 'the product code must be a numerical string'


class VersionValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Version', Offsets.VERSION,
                                            Lengths.VERSION))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        version = int(data.hex()[1], 16)

        assert (version >= 0) and (version <= 15), \
                f"unknown version '{version}'"


class RegionCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Region code', Offsets.REGION_CODE,
                                            Lengths.REGION_CODE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        region_code = int(data.hex()[0], 16)

        assert (region_code >= RegionCode.SMS_JAPAN.value) and \
            (region_code <= RegionCode.GG_INTERNATIONAL.value), \
            f"unknown region code '{region_code}'"


class RomSizeCalc:

    _ROM_SIZE_TABLE = {
        RomSize.SIZE_8KB.value: (8 * 1024),
        RomSize.SIZE_16KB.value: (16 * 1024),
        RomSize.SIZE_32KB.value: (32 * 1024),
        RomSize.SIZE_64KB.value: (64 * 1024),
        RomSize.SIZE_128KB.value: (128 * 1024),
        RomSize.SIZE_256KB.value: (256 * 1024),
        RomSize.SIZE_1MB.value: (1024 * 1024)
    }

    @staticmethod
    def get_real_size(rom_buffer):
        return len(rom_buffer)

    @classmethod
    def get_virtual_size(cls, rom_buffer):
        start_offs = Offsets.ROM_SIZE.value
        end_offs = start_offs + Lengths.ROM_SIZE.value
        data = rom_buffer[start_offs:end_offs]

        return cls.get_virtual_size_from_field(data)

    @classmethod
    def get_virtual_size_from_field(cls, rom_size):
        idx = int(rom_size.hex()[1], 16)

        return cls._ROM_SIZE_TABLE[idx]


class RomSizeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('ROM size', Offsets.ROM_SIZE,
                                            Lengths.ROM_SIZE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        real = RomSizeCalc.get_real_size(rom_buffer)
        virtual = RomSizeCalc.get_virtual_size_from_field(data)

        assert virtual == real, f'{virtual} != {real}'


def check(rom_file):
    validators = [
        TmrSegaValidator(),
        ReservedSpaceValidator(),
        ChecksumValidator(),
        ProductCodeValidator(),
        VersionValidator(),
        RegionCodeValidator(),
        RomSizeValidator()
    ]

    with open(rom_file, 'rb') as f:
        data = f.read()

        for val in validators:
            val.check(data)


def main(args):
    if args.check:
        check(args.rom_file)


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-c', '--check', action='store_true',
                        help='check the ROM coherence')
    parser.add_argument('-f', '--rom-file', metavar='file', help='ROM file',
                        required=True)

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args:
        main(args)
