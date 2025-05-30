from construct.core import (
    Array,
    BitsSwapped,
    BitStruct,
    Const,
    Enum,
    Flag,
    Int8sl,
    Int8ul,
    Int16ul,
    Int32ul,
    Padding,
    Struct,
)

ConsumableType = Enum(
    Int8ul,
    RESTORE_HP = 0,
    RESTORE_MP = 1,
    CURE_STATUS = 2,
    LOSE_HP = 3,
    UNUSABLE = 4,
)

Consumable = Struct(
    item_id=Int16ul,
    icon=Int16ul,
    price=Int32ul,
    type=ConsumableType,
    unk0=Int8ul,
    var_a=Int16ul,
    _const0=Const(0, Int32ul),
)

WeaponAttackType = Enum(
    Int8ul,
    SLASH = 0,
    OVERHEAD = 1,
    SPEAR = 2,
    FIST = 3,
    GUN = 4,
    VALMANWAY = 5,
)

WeaponModifiers = BitsSwapped(BitStruct(
    slash=Flag,
    flame=Flag,
    water=Flag,
    thunder=Flag,
    dark=Flag,
    holy=Flag,
    poison=Flag,
    curse=Flag,
    stone=Flag,
    _padding0=Padding(2),
    swap_hp_mp=Flag,
    half_damage=Flag,
    no_land_cancel=Flag,
    _padding1=Padding(2),
))

Weapon = Struct(
    item_id=Int16ul,
    icon=Int16ul,
    price=Int32ul,
    type=WeaponAttackType,
    unk0=Int8ul,
    attack=Int8ul,
    defense=Int8ul,
    strength=Int8sl,
    constitution=Int8sl,
    intelligence=Int8sl,
    luck=Int8sl,
    modifiers=WeaponModifiers,
    gfx_index=Int8ul,
    sprite_index=Int8ul,
    unk1=Int8ul,
    palette=Int8ul,
    animation=Int8ul,
    iframes=Int8ul,
    sound=Int16ul,
    unk2=Int16ul,
)

ArmorType = Enum(
    Int8ul,
    ARMOR = 0,
    ACCESSORY = 1,
)

ArmorResistances = BitsSwapped(BitStruct(
    slash=Flag,
    flame=Flag,
    water=Flag,
    thunder=Flag,
    dark=Flag,
    holy=Flag,
    poison=Flag,
    curse=Flag,
    stone=Flag,
    _padding=Padding(7),
))

Armor = Struct(
    item_id=Int16ul,
    icon=Int16ul,
    price=Int32ul,
    type=ArmorType,
    unk0=Int8ul,
    attack=Int8ul,
    defense=Int8ul,
    strength=Int8sl,
    constitution=Int8sl,
    intelligence=Int8sl,
    luck=Int8sl,
    resistances=ArmorResistances,
    unk1=Int8ul,
    unk2=Int8ul,
)

ItemTable = Struct(
    consumables=Array(0x20, Consumable),
    weapons=Array(0x3B, Weapon),
    armor=Array(0x2D, Armor),
)
