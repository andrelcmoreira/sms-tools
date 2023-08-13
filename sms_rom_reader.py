from abc import ABC, abstractmethod
from argparse import ArgumentParser
from colorama import Fore
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
    PRODUCT_CODE = 3 # 2.5 bytes
    VERSION = 1 # 0.5 bytes
    REGION_CODE = 1 # 0.5 bytes
    ROM_SIZE = 1 # 0.5 bytes


class FieldValidator(ABC):

    def __init__(self, name, offset, size):
        self._field_name = name
        self._offset = offset.value
        self._size = size.value

    @abstractmethod
    def check(self, data, rom_buffer):
        pass

    @staticmethod
    def show_result(func):
        def wrapper(self, rom_buffer):
            try:
                data = rom_buffer[self._offset:(self._offset + self._size)]
                func(self, data, rom_buffer)

                print('[' + Fore.GREEN + '  OK  ' + Fore.RESET + '] '
                      + self._field_name)
            except AssertionError as e:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self._field_name + '...' + str(e))
            except UnicodeDecodeError:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self._field_name)

        return wrapper


class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'TMR SEGA', Offsets.TMR_SEGA,
                                Lengths.TMR_SEGA)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = b'TMR SEGA'

        assert expected == data, f'{data.decode()} != {expected.decode()}'


class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Reserved space', Offsets.RESERVED_SPACE,
                                Lengths.RESERVED_SPACE)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = [b'\x00\x00', b'\xff\xff', b'\x20\x20']

        assert (data == expected[0]) or (data == expected[1]) \
                or (data == expected[2]), \
                "the reserved space must be '0x0000', '0xffff' or '0x2020'"


class ChecksumValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Checksum', Offsets.CHECKSUM,
                                Lengths.CHECKSUM)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        checksum = self._calculate_checksum(rom_buffer)

        assert data == checksum, f'0x{data.hex()} != 0x{checksum.hex()}'

    def _calculate_checksum(self, rom):
        page_size = 0x4000 # size of page
        start_offset = 0x8000 # first address after header
        remaining_pages = int(len(rom) / page_size) - 3 # number of pages after header
        cksum = self._checksum(rom, 0, Offsets.TMR_SEGA.value, 0) # checksum of first two pages

        for _ in range(remaining_pages, -1, -1):
            cksum = self._checksum(rom, cksum, page_size, start_offset)
            start_offset += 0x4000

        return cksum.to_bytes(Lengths.CHECKSUM.value, byteorder='little')

    def _checksum(self, buffer, cc_last, start_addr, index):
        cs1 = (cc_last >> 8) & 0xff
        cs2 = cc_last & 0xff
        cs3 = e = ov1 = ov2 = 0

        for i in range(index, start_addr + index):
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

        cc_last = (cs1 << 8) & 0xff00 | cs2

        return cc_last & 0xffff


class ProductCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Product code', Offsets.PRODUCT_CODE,
                                Lengths.PRODUCT_CODE)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        code = data.hex()[0:5]

        assert code.isdigit(), 'the product code must be a numerical string'


class VersionValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Version', Offsets.VERSION,
                                Lengths.VERSION)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        version = int(data.hex()[1], 16)

        assert (version >= 0) and (version <= 15), \
                f"unknown version '{version}'"


class RegionCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Region code', Offsets.REGION_CODE,
                                Lengths.REGION_CODE)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        region_code = int(data.hex()[0], 16)

        assert (region_code >= RegionCode.SMS_JAPAN.value) and \
            (region_code <= RegionCode.GG_INTERNATIONAL.value), \
            f"unknown region code '{region_code}'"


class RomSizeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'ROM size', Offsets.ROM_SIZE,
                                Lengths.ROM_SIZE)

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        rom_size_entry = int(data.hex()[1], 16)
        rom_size_map = {
            RomSize.SIZE_8KB.value: (8 * 1024),
            RomSize.SIZE_16KB.value: (16 * 1024),
            RomSize.SIZE_32KB.value: (32 * 1024),
            RomSize.SIZE_64KB.value: (64 * 1024),
            RomSize.SIZE_128KB.value: (128 * 1024),
            RomSize.SIZE_256KB.value: (256 * 1024),
            RomSize.SIZE_1MB.value: (1024 * 1024)
        }

        assert rom_size_map[rom_size_entry] == len(rom_buffer), \
            f'{rom_size_map[rom_size_entry]} != {len(rom_buffer)}'


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
