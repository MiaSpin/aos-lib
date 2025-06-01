from enum import Enum

from aos_lib.structs.lzss import Lzss
from aos_lib.structs.rom_object import RomObject
from aos_lib.structs.tileset import Tileset, TilesetType


class RoomTile(RomObject):
    def __init__(self, rom, tileset: Tileset, offset = None):
        super().__init__(rom, offset)
        self.tileset = tileset

        data = self._stream.read_int(2)
        self.tile_index         = data >> 2
        self.flipped_horizontal = data & 0b00000010 > 0
        self.flipped_vertical   = data & 0b00000001 > 0


class RoomLayer(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.z_index = self._stream.read_int()
        self.scroll_mode = self._stream.read_int()
        self.bg_control = self._stream.read_int(2)
        self.width = self._stream.read_int(2)
        self.height = self._stream.read_int(2)

        # metadata
        metadata_fallback, _ = self._stream.read_and_seek()
        self.width2 = self._stream.read_int()
        self.height2 = self._stream.read_int()

        self.tileset_type = TilesetType(self._stream.read_int(2))
        tileset_fallback, tileset_offset = self._stream.read_and_seek()
        self.tileset = rom.get_tileset(self.tileset_type, tileset_offset)
        self._stream.seek(tileset_fallback)

        self.collision_offset = self._stream.read_offset()

        self.tiles = self._stream.read_array(
            rom=rom,
            element_type=RoomTile,
            count=64 * self.width2 * self.height2,
            offset=self._stream.read_offset(),
            tileset=self.tileset
        )
        self._stream.seek(metadata_fallback)


class Graphics(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        is_compressed = self._stream.read_bool()
        self.bpp = self._stream.read_int()
        self._unk0 = self._stream.read_int()
        self.size = self._stream.read_int()

        if is_compressed:
            fallback, _ = self._stream.read_and_seek()
            data = Lzss.decode(self._stream).getvalue()
            self._stream.seek(fallback)

        self.pixels = []
        if self.bpp == 4:
            for b in data:
                self.pixels.append(b & 0b00001111)
                self.pixels.append(b >> 4)
        else:
            raise ValueError(f"Unsupported BPP {hex(self._stream.tell())} {self.bpp}")


class RoomGraphics(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        fallback, _ = self._stream.read_and_seek()
        self.graphics = Graphics(rom)
        self._stream.seek(fallback)
        self.load_offset = self._stream.read_int()
        self.first_index = self._stream.read_int()
        self.count = self._stream.read_int()
        self.unk0 = self._stream.read_int()


class EntityType(Enum):
    NOTHING = 0
    ENEMY = 1
    SPECIAL_OBJECT = 2
    CANDLE = 3
    PICKUP = 4
    HARDMODE_PICKUP = 5
    ALLSOULS_PICKUP = 6


class Entity(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.x_pos = self._stream.read_int(2)
        self.y_pos = self._stream.read_int(2)
        self.unique_id = self._stream.read_int()
        self.type = EntityType(self._stream.read_int())
        self.subtype = self._stream.read_int()
        self.instaload = self._stream.read_int()
        self.var_a = self._stream.read_int(2)
        self.var_b = self._stream.read_int(2)


class Door(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.destination_room = self._stream.read_int(4)
        self.x_pos = self._stream.read_int()
        self.y_pos = self._stream.read_int()
        self.dest_x_offset = self._stream.read_int(2)
        self.dest_y_offset = self._stream.read_int(2)
        self.dest_x_pos = self._stream.read_int(2)
        self.dest_y_pos = self._stream.read_int(2)
        self._stream.seek(2, 1) # padding


class Room(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.lcd_control = self._stream.read_int(2)
        if self._stream.read_int(2) != 0xFFFF:
            raise TypeError("Not a room")
        self._stream.seek(4, 1) # padding

        fallback, _ = self._stream.read_and_seek()
        self.layer_list = self._stream.read_array(rom, RoomLayer, 3)
        self._stream.seek(fallback)

        fallback, _ = self._stream.read_and_seek()
        self.graphics_pages = self._stream.read_terminated_array(rom, RoomGraphics)
        self._stream.seek(fallback)

        self.palette_page_list = self._stream.read_offset()

        fallback, _ = self._stream.read_and_seek()
        self.entity_list = self._stream.read_terminated_array(rom, Entity, terminator=b'\xFF\x7F\xFF\x7F')
        self._stream.seek(fallback)

        fallback, _ = self._stream.read_and_seek()
        self.door_list = []
        while self._stream.peek(8) < b'\xFF\xFF\x00\x00':
            self.door_list.append(Door(self))
        self._stream.seek(fallback)

        self.unk0 = self._stream.read_int(2)
        self.color_effects = self._stream.read_int(2)
        self.unk1 = self._stream.read_int(4)
