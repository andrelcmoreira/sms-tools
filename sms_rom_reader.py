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
    PRODUCT_CODE = 3 # 2.5 bytes
    VERSION = 1 # 0.5 bytes
    REGION_CODE = 1 # 0.5 bytes
    ROM_SIZE = 1 # 0.5 bytes

class FieldValidator:

    def __init__(self, offset, size, expected):
        self._offset = offset.value
        self._size = size.value
        self._expected = expected

    def check(self, rom_buffer):
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert self._expected == data

class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Offsets.TMR_SEGA, Lengths.TMR_SEGA,
                                b'TMR SEGA')

class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Offsets.RESERVED_SPACE,
                                Lengths.RESERVED_SPACE,
                                [b'\x00\x00', b'\xff\xff', b'\x20\x20'])

    def check(self, rom_buffer):
        data = rom_buffer[self._offset:(self._offset + self._size)]

        assert (data == self._expected[0]) or (data == self._expected[1]) or \
                (data == self._expected[2])

_VALIDATORS = [
    TmrSegaValidator(),
    ReservedSpaceValidator()
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
