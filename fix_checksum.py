from sys import argv

from sms.checksum import ChecksumCalc
from sms.constants import Offsets, Lengths


def fix_checksum(rom_file):
    with open(rom_file, 'r+b') as f:
        print('[*] loading rom...', end='')
        data = f.read()
        print('OK!')

        print('[*] calculating checksum...', end='')
        cksum = ChecksumCalc.calculate(data)
        print('OK!')

        print('[*] patching rom...', end='')
        f.seek(Offsets.CHECKSUM.value)
        f.write(cksum)
        print('OK!')


def main():
    try:
        fix_checksum(argv[1])
    except PermissionError:
        print('ERROR! permission denied')
    except KeyError:
        print(f'usage: {argv[0]} rom_file')
    
    
if __name__ == "__main__":
    main()