from argparse import ArgumentParser
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

class Lengths(Enum):
    TMR_SEGA = 8
    RESERVED_SPACE = 2
    CHECKSUM = 2
    PRODUCT_CODE = 2.5
    VERSION = 0.5
    REGION_CODE = 0.5
    ROM_SIZE = 0.5

class FieldValidator:

    def __init__(self, offset, size, expected):
        self._offset = offset
        self._size = size
        self._expected = expected

    def check(self, rom_buffer):
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert self._expected == data

class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Offsets.TMR_SEGA.value,
                                Lengths.TMR_SEGA.value, b'TMR SEGA')

_VALIDATORS = [
    TmrSegaValidator()
]

def main(rom_file):
    with open(rom_file, 'rb') as f:
        data = f.read()

        for field in _VALIDATORS:
            field.check(data)

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
