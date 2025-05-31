from enum import Enum

from aos_lib.structs.rom_object import RomObject


class EntityType(Enum):
    NOTHING = 0,
    ENEMY = 1,
    SPECIAL_OBJECT = 2,
    CANDLE = 3,
    PICKUP = 4,
    HARDMODE_PICKUP = 5,
    ALLSOULS_PICKUP = 6,


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
        self.layer_list_offset = self._stream.read_offset()
        self.gfx_page_offset = self._stream.read_offset()
        self.palette_page_list = self._stream.read_offset()
        self.entity_list = rom.read_terminated_array(Entity, self._stream.read_offset(), b'\x7F\xFF\x7F\xFF')

        fallback = self._stream.tell()
        self._stream.seek(self._stream.read_offset())
        self.door_list = []
        while self._stream.peek(8) < b'\xFF\xFF\x00\x00':
            self.door_list.append(Door(self))
        self._stream.seek(fallback)

        self.unk0 = self._stream.read_int(2)
        self.color_effects = self._stream.read_int(2)
        self.unk1 = self._stream.read_int(4)
