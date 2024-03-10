from core.constants import Offsets, Lengths
from core.size import SizeCalc


_PAGE_SIZE = 0x4000


def calculate(rom):
    # first page address after the rom header
    start_addr = Offsets.ROM_SIZE.value + 1
    # number of pages after header
    rem_pages = int(SizeCalc.get_virtual_size(rom) / _PAGE_SIZE) - 2
    # checksum of first two pages
    cksum = _checksum(rom, 0, 0, Offsets.TMR_SEGA.value)

    for _ in range(0, rem_pages):
        cksum = _checksum(rom, cksum, start_addr, _PAGE_SIZE)
        start_addr += _PAGE_SIZE

    return cksum.to_bytes(Lengths.CHECKSUM.value, byteorder='little')


def _checksum(buffer, last_cksum, start_range, offset):
    cs1 = (last_cksum >> 8) & 0xff
    cs2 = last_cksum & 0xff
    cs3 = e = ov1 = ov2 = 0

    for i in range(start_range, start_range + offset):
        e = cs2
        ov1 = e
        e += buffer[i]
        ov2 = e & 0xff

        if ov1 > ov2:
            cs3 = 1

        cs2 = e & 0xff
        e = cs1 + cs3
        cs3 = 0
        cs1 = e

    last_cksum = (cs1 << 8) & 0xff00 | cs2

    return last_cksum & 0xffff
