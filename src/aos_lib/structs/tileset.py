
from aos_lib.stream import RomStream
from aos_lib.structs.rom_object import RomObject


class Tile(RomObject):
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
    def __init__(self, rom, stream: RomStream, offset = None):
        super().__init__(rom, offset)

        tile_count = stream.getbuffer().nbytes // 2
        self.tiles = []
        for i in range(tile_count):
            self.tiles.append(Tile(rom, stream))
