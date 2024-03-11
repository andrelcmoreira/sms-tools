from sys import argv

from core.sdsc_header import Offsets, Lengths


def dump_headers(rom_file):
    # TODO
    pass


if __name__ == '__main__':
    if len(argv) > 1:
        dump_headers(argv[1])
    else:
        print(f'usage: {argv[0]} <rom_file>')
