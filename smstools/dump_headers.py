from sys import argv

from core.sdsc_header import SdscHeader
from core.rom_header import RomHeader


def dump_headers(header_type, rom_file):
    with open(rom_file, 'rb') as f:
        data = f.read()

        match header_type:
            case 'rom-header':
                print(RomHeader(data))
            case 'sdsc':
                print(SdscHeader(data))
            case 'all':
                print(RomHeader(data))
                print('')
                print(SdscHeader(data))


if __name__ == '__main__':
    match len(argv):
        case 3: dump_headers(argv[1], argv[2])
        case _: print(f'usage: {argv[0]} <rom-header|sdsc|all> <rom-file>')
