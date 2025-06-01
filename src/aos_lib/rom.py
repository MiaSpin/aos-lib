from pathlib import Path

from aos_lib.stream import RomStream
from aos_lib.structs.lzss import Lzss
from aos_lib.structs.room import Entity
from aos_lib.structs.tileset import Tileset


class Rom:
    _stream: RomStream
    _modified_entities: dict[int, Entity]

    def __init__(self, rom_path: Path) -> None:
        with rom_path.open("rb") as rom:
            self._stream = RomStream(rom.read())

        self._modified_entities = {}
        self.modified_tilesets = {}


    def get_entity(self, offset: int) -> Entity:
        if offset in self._modified_entities:
            return self._modified_entities[offset]
        entity = Entity(self, offset)
        self._modified_entities[offset] = entity
        return entity

    def get_tileset(self, offset: int) -> Tileset:
        if offset in self.modified_tilesets:
            return self.modified_tilesets[offset]

        tileset = Tileset(self, Lzss.decode(self._stream, offset))
        self.modified_tilesets[offset] = tileset
        return tileset
