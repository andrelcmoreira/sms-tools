from sys import argv

from core.code_masters_header import CodeMastersHeader
from core.rom_header import RomHeader
from core.sdsc_header import SdscHeader


def dump_headers(header_type: str, rom_file: str):
    with open(rom_file, 'rb') as f:
        data = f.read()

        match header_type:
            case 'all':
                print(RomHeader(data), '\n')
                print(SdscHeader(data), '\n')
                print(CodeMastersHeader(data))
            case 'rom-header':
                print(RomHeader(data))
            case 'codemasters':
                print(CodeMastersHeader(data))
            case 'sdsc':
                print(SdscHeader(data))


if __name__ == '__main__':
    match len(argv):
        case 3: dump_headers(argv[1], argv[2])
        case _: print(
            f'usage: {argv[0]} <rom-header|codemasters|sdsc|all> <rom-file>')
