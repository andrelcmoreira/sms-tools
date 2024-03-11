from sys import argv

from core.checksum import calculate
from core.rom_header import Offsets


def fix_checksum(rom_path):
    print('[*] loading rom...')

    with open(rom_path, 'r+b') as rom_file:
        data = rom_file.read()

        print('[*] calculating checksum...')
        cksum = calculate(data)

        print('[*] patching rom...')
        rom_file.seek(Offsets.CHECKSUM.value)
        rom_file.write(cksum)


if __name__ == '__main__':
    if len(argv) > 1:
        fix_checksum(argv[1])
    else:
        print(f'usage: {argv[0]} <rom_file>')
