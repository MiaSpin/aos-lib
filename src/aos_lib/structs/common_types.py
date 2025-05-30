from construct.core import Pointer, Subconstruct, stream_read


class AosPointer(Subconstruct):
    def _parse(self, stream, context, path):
        # the most significant byte of offsets in AoS are 0x08
        offset = int.from_bytes(stream_read(stream, 4, path), 'little') - 0x08000000
        return Pointer(offset, self.subcon)._parsereport(stream, context, path)
