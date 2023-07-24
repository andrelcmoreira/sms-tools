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

def main(rom_file):
    with open(rom_file, 'rb') as f:
        pass

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
