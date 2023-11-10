from argparse import ArgumentParser
from sys import argv


def get_assets(rom_file, output_dir):
    with open(rom_file, 'rb') as f:
        data = f.read()

        pass # TODO(andrelcmoreira) implement me


def parse_args():
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('-f', '--rom-file', metavar='file', help='ROM file',
                        required=True)
    parser.add_argument('-o', '--output-dir', metavar='directory',
                        help='output directory to place the assets on')

    # no arguments provided
    if len(argv) == 1:
        parser.print_help()
        return None

    return parser.parse_args()


def main():
    args = parse_args()

    if args:
        get_assets(args.rom_file, args.output_dir)


if __name__ == "__main__":
    main()
