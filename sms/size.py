from sms.constants import RomSize, Offsets, Lengths


class SizeCalc:

    _ROM_SIZE_TABLE = {
        RomSize.SIZE_8KB.value: (8 * 1024),
        RomSize.SIZE_16KB.value: (16 * 1024),
        RomSize.SIZE_32KB.value: (32 * 1024),
        RomSize.SIZE_64KB.value: (64 * 1024),
        RomSize.SIZE_128KB.value: (128 * 1024),
        RomSize.SIZE_256KB.value: (256 * 1024),
        RomSize.SIZE_1MB.value: (1024 * 1024)
    }

    @staticmethod
    def get_real_size(rom_buffer):
        return len(rom_buffer)

    @classmethod
    def get_virtual_size(cls, rom_buffer):
        start_offs = Offsets.ROM_SIZE.value
        end_offs = start_offs + Lengths.ROM_SIZE.value
        data = rom_buffer[start_offs:end_offs]

        return cls.get_virtual_size_from_field(data)

    @classmethod
    def get_virtual_size_from_field(cls, rom_size):
        idx = int(rom_size.hex()[1], 16)

        return cls._ROM_SIZE_TABLE[idx]
