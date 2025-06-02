from enum import Enum

from aos_lib.structs.rom_object import RomObject


class ConsumableType(Enum):
    RESTORE_HP = 0
    RESTORE_MP = 1
    CURE_STATUS = 2
    LOSE_HP = 3
    UNUSABLE = 4


class Consumable(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.item_id = self._stream.read_int(2)
        self.icon = self._stream.read_int(2)
        self.price = self._stream.read_int(4)
        self.type = ConsumableType(self._stream.read_int())
        self.unk0 = self._stream.read_int()
        self.var_a = self._stream.read_int(2)
        self._const0 = self._stream.read_int(4)


class WeaponAttackType(Enum):
    SLASH = 0
    OVERHEAD = 1
    SPEAR = 2
    FIST = 3
    GUN = 4
    VALMANWAY = 5


class WeaponModifiers(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        modifiers = self._stream.read_int(2)
        self.slash          = modifiers & 0b00000000_00000001 > 0
        self.flame          = modifiers & 0b00000000_00000010 > 0
        self.water          = modifiers & 0b00000000_00000100 > 0
        self.thunder        = modifiers & 0b00000000_00001000 > 0
        self.dark           = modifiers & 0b00000000_00010000 > 0
        self.holy           = modifiers & 0b00000000_00100000 > 0
        self.poison         = modifiers & 0b00000000_01000000 > 0
        self.curse          = modifiers & 0b00000000_10000000 > 0
        self.stone          = modifiers & 0b00000001_00000000 > 0
        self.swap_hp_mp     = modifiers & 0b00001000_00000000 > 0
        self.half_damage    = modifiers & 0b00010000_00000000 > 0
        self.no_land_cancel = modifiers & 0b00100000_00000000 > 0


class Weapon(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.item_id = self._stream.read_int(2)
        self.icon = self._stream.read_int(2)
        self.price = self._stream.read_int(4)
        self.type = WeaponAttackType(self._stream.read_int())
        self.unk0 = self._stream.read_int()
        self.attack = self._stream.read_int()
        self.defense = self._stream.read_int()
        self.strength = self._stream.read_int()
        self.constitution = self._stream.read_int()
        self.intelligence = self._stream.read_int()
        self.luck = self._stream.read_int()
        self.modifiers = WeaponModifiers(self._stream.read_int(2))
        self.gfx_index = self._stream.read_int()
        self.sprite_index = self._stream.read_int()
        self.unk1 = self._stream.read_int()
        self.palette = self._stream.read_int()
        self.animation = self._stream.read_int()
        self.iframes = self._stream.read_int()
        self.sound = self._stream.read_int(2)
        self.unk2 = self._stream.read_int(2)


class ArmorType(Enum):
    ARMOR = 0
    ACCESSORY = 1


class ArmorResistances(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        resist = self._stream.read_int(2)
        self.slash   = resist & 0b00000000_00000001 > 0
        self.flame   = resist & 0b00000000_00000010 > 0
        self.water   = resist & 0b00000000_00000100 > 0
        self.thunder = resist & 0b00000000_00001000 > 0
        self.dark    = resist & 0b00000000_00010000 > 0
        self.holy    = resist & 0b00000000_00100000 > 0
        self.poison  = resist & 0b00000000_01000000 > 0
        self.curse   = resist & 0b00000000_10000000 > 0
        self.stone   = resist & 0b00000001_00000000 > 0


class Armor(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.item_id = self._stream.read_int(2)
        self.icon = self._stream.read_int(2)
        self.price = self._stream.read_int(4)
        self.type = ArmorType(self._stream.read_int())
        self.unk0 = self._stream.read_int()
        self.attack = self._stream.read_int()
        self.defense = self._stream.read_int()
        self.strength = self._stream.read_int()
        self.constitution = self._stream.read_int()
        self.intelligence = self._stream.read_int()
        self.luck = self._stream.read_int()
        self.resistances = ArmorResistances(self._stream.read_int(2))
        self.unk1 = self._stream.read_int()
        self.unk2 = self._stream.read_int()


class RedSoulAnimation(Enum):
    STANDARD = 0
    UPPERCUT = 1
    STRAIGHT_PUNCH = 2
    POWERFUL_PUNCH = 3


class RedSoulDamageType(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        modifiers = self._stream.read_int(2)
        self.slash          = modifiers & 0b00000000_00000001 > 0
        self.flame          = modifiers & 0b00000000_00000010 > 0
        self.water          = modifiers & 0b00000000_00000100 > 0
        self.thunder        = modifiers & 0b00000000_00001000 > 0
        self.dark           = modifiers & 0b00000000_00010000 > 0
        self.holy           = modifiers & 0b00000000_00100000 > 0
        self.poison         = modifiers & 0b00000000_01000000 > 0
        self.curse          = modifiers & 0b00000000_10000000 > 0
        self.stone          = modifiers & 0b00000001_00000000 > 0
        self.swap_hp_mp     = modifiers & 0b00001000_00000000 > 0


class RedSoul(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.code_pointer = self._stream.read_offset()
        self.animation = RedSoulAnimation(self._stream.read_int(2))
        self.mana_cost = self._stream.read_int(2)
        self.max_projectiles = self._stream.read_int()
        self.unk0 = self._stream.read_int()
        self.damage_multiplier = self._stream.read_int(2)
        self.damage_type = RedSoulDamageType(self._stream.read_int(2))
        self.var_pointer = self._stream.read_int(2) # varies based on self.code_pointer


class BlueSoulControlType(Enum):
    HOLD = 1
    TOGGLE = 2


class BlueSoul(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.code_pointer = self._stream.read_offset()
        self.mana_cost = self._stream.read_int()
        self.control_type = BlueSoulControlType(self._stream.read_int())
        self.unk0 = self._stream.read_int(2)
        self.var = self._stream.read_int(4) # varies based on soul


class YellowSoulStat(Enum):
    STRENGTH = 0
    CONSTITUTION = 0
    INTELLIGENCE = 0
    LUCK = 0


class YellowSoul(RomObject):
    def __init__(self, rom, offset = None):
        super().__init__(rom, offset)

        self.code_pointer = self._stream.read_offset()
        self.unk0 = self._stream.read_int(2)
        self.raise_stat = YellowSoulStat(self._stream.read_int())
        self.var = self._stream.read_int(4) # varies based on soul
