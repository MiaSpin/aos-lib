
from enum import Enum

from aos_lib.stream import RomStream
from aos_lib.structs.lzss import Lzss
from aos_lib.structs.rom_object import RomObject


class TilesetType(Enum):
    UNCOMPRESSED = 1
    COMPRESSED = 2


class TilesetTile(RomObject):
    index: int
    page: int
    palette: int
    flipped_horizontal: bool
    flipped_vertical: bool

    def __init__(self, rom, stream: RomStream, offset = None):
        super().__init__(rom, offset)

        self.tile_index = stream.read_int()
        metadata = stream.read_int()
        self.page =    metadata & 0b00000011
        self.h_flip =  metadata & 0b00000100 > 0
        self.v_flip =  metadata & 0b00001000 > 0
        self.palette = metadata & 0b11110000 >> 4


class Tileset(RomObject):
    def __init__(self, rom, offset = None, *, tileset_type: TilesetType):
        super().__init__(rom, offset)

        if tileset_type is TilesetType.COMPRESSED:
            uncompressed_stream = Lzss.decode(self._stream, None)
            tile_count = uncompressed_stream.getbuffer().nbytes // 2
            self.tiles = []
            for i in range(tile_count):
                self.tiles.append(TilesetTile(rom, uncompressed_stream))
        else:
            for i in range(4096):
                self.tiles.append(TilesetTile(rom))
