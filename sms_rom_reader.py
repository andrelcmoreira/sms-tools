from argparse import ArgumentParser
from colorama import Fore
from enum import Enum
from sys import argv
from abc import ABC, abstractmethod

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
    def check(self, rom_buffer):
        pass

    @staticmethod
    def show_result(func):
        def wrapper(self, rom_buffer):
            try:
                func(self, rom_buffer)

                print('[' + Fore.GREEN + '   OK  ' + Fore.RESET + '] '
                      + self._field_name)
            except AssertionError:
                print('[' + Fore.RED + ' ERROR ' + Fore.RESET + '] '
                      + self._field_name)

        return wrapper

class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'TMR SEGA', Offsets.TMR_SEGA,
                                Lengths.TMR_SEGA)

    @FieldValidator.show_result
    def check(self, rom_buffer):
        expected = b'TMR SEGA'
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert expected == data

class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Reserved space', Offsets.RESERVED_SPACE,
                                Lengths.RESERVED_SPACE)

    @FieldValidator.show_result
    def check(self, rom_buffer):
        expected = [b'\x00\x00', b'\xff\xff', b'\x20\x20']
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert (data == expected[0]) or (data == expected[1]) \
                or (data == expected[2])

class ChecksumValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, 'Checksum', Offsets.CHECKSUM,
                                Lengths.CHECKSUM)

    @FieldValidator.show_result
    def check(self, rom_buffer):
        expected = self._calculate_checksum(rom_buffer)
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert data == expected

    @staticmethod
    def _calculate_checksum(rom_buffer):
        return 0 # TODO

def main(rom_file):
    validators = [
        TmrSegaValidator(),
        ReservedSpaceValidator(),
        ChecksumValidator()
    ]

    with open(rom_file, 'rb') as f:
        data = f.read()

        for val in validators:
            val.check(data)

def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-r', '--rom-file', metavar='file',
                        help='ROM file')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args:
        main(args.rom_file)
