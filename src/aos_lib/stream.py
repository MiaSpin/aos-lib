from io import BytesIO


class RomStream(BytesIO):
    def read_int(self, size: int = 1) -> int:
        return int.from_bytes(self.read(size), 'little')

    def read_offset(self) -> int:
        # the most significant byte of offsets in AoS is always 0x08
        return self.read_int(4) - 0x08000000

    def read_and_seek(self) -> int:
        fallback = self.tell()
        self.seek(self.read_offset())
        return fallback

    def peek(self, size: int = 1) -> bytes:
        peeked = self.read(size)
        self.seek(-size, 1)
        return peeked
