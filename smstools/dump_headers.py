from sys import argv

from core.sdsc_header import SdscHeader
from core.rom_header import RomHeader


def dump_headers(header_type, rom_file):
    header = None

    with open(rom_file, 'rb') as f:
        data = f.read()

        match header_type:
            case 'rom-header':
                header = RomHeader(data)
            case 'sdsc':
                header = SdscHeader(data)

    if header:
        print(header)


if __name__ == '__main__':
    if len(argv) > 2:
        dump_headers(argv[1], argv[2])
    else:
        print(f'usage: {argv[0]} <rom-header|sdsc> <rom-file>')
