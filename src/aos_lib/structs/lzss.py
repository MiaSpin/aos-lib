from aos_lib.stream import RomStream


class Lzss:
    @staticmethod
    def decode(stream: RomStream, offset: int | None = None) -> RomStream:
        if offset is not None:
            stream.seek(offset)

        header = stream.read(4)
        if header[0] != 0x10:
            raise TypeError("Stream is not LZSS compressed data.")

        uncompressed_size = int.from_bytes(header, 'little') >> 8
        data = bytearray()
        while len(data) < uncompressed_size:
            # this LZSS implementation uses a bitfield to indicate whether each of the
            # next 8 bytes are literal or encoded, where 0 = literal and 1 = encoded
            block_header = stream.read_int()
            current_bit = 0x80
            while current_bit > 0:
                if block_header & current_bit:
                    encoded_data = stream.read_int(2)
                    distance = encoded_data & 0xFFF
                    length = (encoded_data >> 12) + 3
                    data += data[-distance - 1:-distance] * length
                else:
                    data.append(stream.read_int())

                if len(data) == uncompressed_size:
                    break
                current_bit >>= 1

        return RomStream(bytes(data[4:]))
