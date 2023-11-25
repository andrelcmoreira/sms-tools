from argparse import ArgumentParser
from sys import argv

from sms.checksum import ChecksumCalc
from sms.constants import Offsets, Lengths


def fix_checksum(rom_file):
    with open(rom_file, 'r+b') as f:
        data = f.read()

        print('[*] calculating checksum...')
        cksum = ChecksumCalc.calculate(data)

        print('[*] patching rom file...')
        f.seek(Offsets.CHECKSUM.value)
        f.write(cksum)


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-f', '--rom-file', metavar='file', help='ROM file',
                        required=True)

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main():
    args = parse_args()

    if args:
        fix_checksum(args.rom_file)


if __name__ == "__main__":
    main()
