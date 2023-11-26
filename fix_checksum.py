from sys import argv

from sms.checksum import ChecksumCalc
from sms.constants import Offsets, Lengths


def fix_checksum(rom_file):
    try:
        print('[*] loading rom...', end='')

        with open(rom_file, 'r+b') as f:
            data = f.read()
            print('OK!')

            print('[*] calculating checksum...', end='')
            cksum = ChecksumCalc.calculate(data)
            assert int.from_bytes(cksum) > 0, \
                'fail to compute the rom checksum!'
            print('OK!')

            print('[*] patching rom...', end='')
            assert len(data) > Offsets.CHECKSUM.value, \
                'the specified rom file has an invalid size!'
            f.seek(Offsets.CHECKSUM.value)
            f.write(cksum)
            print('OK!')
            print('[*] done!')
    except PermissionError:
        print('ERROR: permission denied!')
    except AssertionError as e:
        print('ERROR: %s' % str(e))

    
if __name__ == "__main__":
    if len(argv) > 1:
        fix_checksum(argv[1])
    else:
        print('usage: %s <rom_file>' % argv[0])