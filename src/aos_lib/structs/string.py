from construct.core import Array, Construct, Int8ul, Peek, Struct, stream_read

from aos_lib.structs.common_types import AosPointer

SPECIAL_CHARACTERS = {
    0x90: "Œ",
    0x91: "œ",
    0xA7: "§",
    0xAA: "ᵃ",
    0xAB: "«",
    0xBA: "°",
    0xBB: "»",
    0xC0: "À",
    0xC1: "Á",
    0xC2: "Â",
    0xC4: "Ä",
    0xC7: "Ç",
    0xC8: "È",
    0xC9: "É",
    0xCA: "Ê",
    0xCB: "Ë",
    0xD6: "Ö",
    0xD8: "Œ",
    0xDB: "Û",
    0xDC: "Ü",
    0xDF: "ß",
    0xE0: "à",
    0xE2: "â",
    0xE4: "ä",
    0xE7: "ç",
    0xE8: "è",
    0xE9: "é",
    0xEA: "ê",
    0xEB: "ë",
    0xEE: "î",
    0xEF: "ï",
    0xF4: "ô",
    0xF6: "ö",
    0xF9: "ù",
    0xFB: "û",
    0xFC: "ü",
}


class AosString(Construct):
    def _parse(self, stream, context, path):
        # all strings start with 0x0100, this can be discarded
        stream_read(stream, 2, path)

        string = ""
        while Peek(Int8ul)._parsereport(stream, context, path) != 0x0A:
            charcode = int.from_bytes(stream_read(stream, 1, path))
            if charcode == 0x06:
                string += "\n"
            # standard ascii characters
            elif 0x20 <= charcode <= 0x7E:
                string += chr(charcode)
            elif charcode in SPECIAL_CHARACTERS:
                string += SPECIAL_CHARACTERS[charcode]

        return string


Localization = Struct(
    character_names=Array(11, AosPointer(AosString())),
    dialogue=Array(80, AosPointer(AosString())),
    item_names=Array(136, AosPointer(AosString())),
    red_soul_names=Array(55, AosPointer(AosString())),
    blue_soul_names=Array(25, AosPointer(AosString())),
    yellow_soul_names=Array(35, AosPointer(AosString())),
    grey_soul_names=Array(6, AosPointer(AosString())),
    item_descriptions=Array(136, AosPointer(AosString())),
    red_soul_descriptions=Array(55, AosPointer(AosString())),
    blue_soul_descriptions=Array(25, AosPointer(AosString())),
    yellow_soul_descriptions=Array(35, AosPointer(AosString())),
    grey_soul_descriptions=Array(6, AosPointer(AosString())),
    enemy_names=Array(113, AosPointer(AosString())),
    enemy_descriptions=Array(113, AosPointer(AosString())),
    menu=Array(84, AosPointer(AosString())),
    music_tracks=Array(29, AosPointer(AosString())),
    misc_menu=Array(7, AosPointer(AosString())),
    misc=Array(13, AosPointer(AosString())),
)

Strings = Struct(
    english=Localization,
    french=Localization,
    german=Localization,
    language_names=Array(3, AosPointer(AosString())),
)
