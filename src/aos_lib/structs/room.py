from construct import this
from construct.core import (
    Const,
    Enum,
    FocusedSeq,
    GreedyRange,
    Int8ul,
    Int16ul,
    Int32ul,
    Padding,
    Peek,
    StopIf,
    Struct,
)

from aos_lib.structs.common_types import AosPointer

EntityType = Enum(
    Int8ul,
    NOTHING = 0,
    ENEMY = 1,
    SPECIAL_OBJECT = 2,
    CANDLE = 3,
    PICKUP = 4,
    HARDMODE_PICKUP = 5,
    ALLSOULS_PICKUP = 6,
)

Entity = Struct(
    "x_pos" / Int16ul,
    "y_pos" / Int16ul,
    "unique_id" / Int8ul,
    "type" / EntityType,
    "subtype" / Int8ul,
    "instaload" / Int8ul,
    "var_a" / Int16ul,
    "var_b" / Int16ul,
)

Door = Struct(
    "destination_room" / Int32ul,
    "x_pos" / Int8ul,
    "y_pos" / Int8ul,
    "dest_x_offset" / Int16ul,
    "dest_y_offset" / Int16ul,
    "dest_x_pos" / Int16ul,
    "dest_y_pos" / Int16ul,
    "_padding" / Padding(2),
)

Room = Struct(
    "lcd_control" / Int16ul,
    "_const0" / Const(b'\xFF\xFF'),
    "_padding" / Padding(4),
    "_layer_list_offset" / Int32ul,
    "_gfx_page_offset" / Int32ul,
    "_palette_page_list" / Int32ul,

    "entity_list" / AosPointer(
        GreedyRange(
            FocusedSeq(
                "entity",
                "peek" / Peek(Int32ul),
                StopIf(this.peek == 0x7FFF7FFF),
                "entity" / Entity,
            ),
        ),
    ),

    "door_list" / AosPointer(
        GreedyRange(
            FocusedSeq(
                "door",
                "peek" / Peek(Int32ul),
                StopIf(this.peek >= 0xFFFF0000),
                "door" / Door,
            ),
        ),
    ),

    "unk0" / Int16ul,
    "color_effects" / Int16ul,
    "unk1" / Int32ul,
)
