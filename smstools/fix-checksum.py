from sys import argv

from core.checksum import calculate
from core.rom_header import Offsets


def fix_checksum(rom_path: str) -> None:
    print('[*] loading rom...')

    with open(rom_path, 'r+b') as rom_file:
        data = rom_file.read()

        print('[*] calculating checksum...')
        cksum = calculate(data)

        print('[*] patching rom...')
        rom_file.seek(Offsets.CHECKSUM.value)
        rom_file.write(cksum)


def main() -> None:
    if len(argv) != 2:
        print(f'usage: {argv[0]} <rom-file>')
        return

    fix_checksum(argv[1])


if __name__ == '__main__':
    main()
