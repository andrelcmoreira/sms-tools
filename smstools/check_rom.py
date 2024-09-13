from abc import ABC, abstractmethod
from dataclasses import dataclass
from sys import argv
from colorama import Fore

from core.checksum import calculate
from core.rom_header import Lengths, Offsets, RegionCode, RomHeader
from core.size import get_real_size, get_virtual_size_from_field


@dataclass
class Field:
    name: str
    offset: Offsets
    size: Lengths


class FieldValidator(ABC):

    def __init__(self, field: Field):
        self.field = field

    @abstractmethod
    def check(self, data: bytes, rom_buffer: bytes):
        pass

    @staticmethod
    def show_result(func):
        def wrapper(self, rom_buffer: bytes):
            hdr = RomHeader(rom_buffer)

            try:
                data = hdr.get_field(self.field.offset.value,
                                     self.field.size.value)
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
        super().__init__(Field('TMR SEGA', Offsets.TMR_SEGA, Lengths.TMR_SEGA))

    @FieldValidator.show_result
    def check(self, data: bytes, _):
        expected = b'TMR SEGA'

        assert data == expected, f'{data.decode()} != {expected.decode()}'


class ReservedSpaceValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('Reserved space', Offsets.RESERVED_SPACE,
                               Lengths.RESERVED_SPACE))

    @FieldValidator.show_result
    def check(self, data: bytes, _):
        expected = [b'\x00\x00', b'\xff\xff', b'\x20\x20']

        assert data in expected, \
            "the reserved space must be '0x0000', '0xffff' or '0x2020'"


class ChecksumValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('Checksum', Offsets.CHECKSUM, Lengths.CHECKSUM))

    @FieldValidator.show_result
    def check(self, data: bytes, rom_buffer: bytes):
        checksum = calculate(rom_buffer)

        assert data == checksum, f'0x{data.hex()} != 0x{checksum.hex()}'


class ProductCodeValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('Product code', Offsets.PRODUCT_CODE,
                               Lengths.PRODUCT_CODE))

    @FieldValidator.show_result
    def check(self, data: bytes, _):
        code = data.hex()[0:5]

        assert code.isdigit(), 'the product code must be a numerical string'


class VersionValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('Version', Offsets.VERSION, Lengths.VERSION))

    @FieldValidator.show_result
    def check(self, data: bytes, _):
        version = int(data.hex()[1], 16)

        assert 0 <= version <= 15, f"unknown version '{version}'"


class RegionCodeValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('Region code', Offsets.REGION_CODE,
                               Lengths.REGION_CODE))

    @FieldValidator.show_result
    def check(self, data: bytes, _):
        region_code = int(data.hex()[0], 16)

        assert RegionCode.SMS_JAPAN.value <= region_code <= \
            RegionCode.GG_INTERNATIONAL.value, \
            f"unknown region code '{region_code}'"


class RomSizeValidator(FieldValidator):

    def __init__(self):
        super().__init__(Field('ROM size', Offsets.ROM_SIZE, Lengths.ROM_SIZE))

    @FieldValidator.show_result
    def check(self, data: bytes, rom_buffer: bytes):
        real = get_real_size(rom_buffer)
        virtual = get_virtual_size_from_field(data)

        assert virtual == real, f'{virtual} != {real}'


def check(rom_file: str):
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
    match len(argv):
        case 2: check(argv[1])
        case _: print(f'usage: {argv[0]} <rom-file>')
