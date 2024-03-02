from abc import ABC, abstractmethod
from dataclasses import dataclass
from sys import argv
from colorama import Fore

from sms.checksum import ChecksumCalc
from sms.size import SizeCalc
from sms.constants import (
    Lengths,
    Offsets,
    RegionCode,
)


@dataclass
class Field:
    name: str
    offset: Offsets
    size: Lengths


class FieldValidator(ABC):

    def __init__(self, field):
        self.field = field

    @abstractmethod
    def check(self, data, rom_buffer):
        pass

    @staticmethod
    def show_result(func):
        def wrapper(self, rom_buffer):
            start_offs = self.field.offset.value
            end_offs = start_offs + self.field.size.value

            try:
                data = rom_buffer[start_offs:end_offs]
                func(self, data, rom_buffer)

                print('[' + Fore.GREEN + '  OK  ' + Fore.RESET + '] '
                      + self.field.name)
            except AssertionError as e:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self.field.name + '...' + str(e))
            except UnicodeDecodeError:
                print('[' + Fore.RED + ' FAIL ' + Fore.RESET + '] '
                      + self.field.name)

        return wrapper


class TmrSegaValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('TMR SEGA', Offsets.TMR_SEGA,
                                            Lengths.TMR_SEGA))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = b'TMR SEGA'

        assert data == expected, f'{data.decode()} != {expected.decode()}'


class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Reserved space',
                                            Offsets.RESERVED_SPACE,
                                            Lengths.RESERVED_SPACE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        expected = [b'\x00\x00', b'\xff\xff', b'\x20\x20']

        assert data in expected, \
            "the reserved space must be '0x0000', '0xffff' or '0x2020'"


class ChecksumValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Checksum', Offsets.CHECKSUM,
                                            Lengths.CHECKSUM))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        checksum = ChecksumCalc.calculate(rom_buffer)

        assert data == checksum, f'0x{data.hex()} != 0x{checksum.hex()}'


class ProductCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Product code',
                                            Offsets.PRODUCT_CODE,
                                            Lengths.PRODUCT_CODE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        code = data.hex()[0:5]

        assert code.isdigit(), 'the product code must be a numerical string'


class VersionValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Version', Offsets.VERSION,
                                            Lengths.VERSION))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        version = int(data.hex()[1], 16)

        assert 0 <= version <= 15, f"unknown version '{version}'"


class RegionCodeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('Region code', Offsets.REGION_CODE,
                                            Lengths.REGION_CODE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        region_code = int(data.hex()[0], 16)

        assert RegionCode.SMS_JAPAN.value <= region_code <= \
            RegionCode.GG_INTERNATIONAL.value, \
            f"unknown region code '{region_code}'"


class RomSizeValidator(FieldValidator):

    def __init__(self):
        FieldValidator.__init__(self, Field('ROM size', Offsets.ROM_SIZE,
                                            Lengths.ROM_SIZE))

    @FieldValidator.show_result
    def check(self, data, rom_buffer):
        real = SizeCalc.get_real_size(rom_buffer)
        virtual = SizeCalc.get_virtual_size_from_field(data)

        assert virtual == real, f'{virtual} != {real}'


def check(rom_file):
    validators = [
        TmrSegaValidator(),
        ReservedSpaceValidator(),
        ChecksumValidator(),
        ProductCodeValidator(),
        VersionValidator(),
        RegionCodeValidator(),
        RomSizeValidator()
    ]

    with open(rom_file, 'rb') as f:
        data = f.read()

        for val in validators:
            val.check(data)


if __name__ == '__main__':
    if len(argv) > 1:
        check(argv[1])
    else:
        print(f'usage: {argv[0]} <rom_file>')
