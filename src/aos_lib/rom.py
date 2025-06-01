from pathlib import Path

from aos_lib.stream import RomStream
from aos_lib.structs.room import Entity, Room
from aos_lib.structs.tileset import Tileset, TilesetType


class Rom:
    _stream: RomStream
    _modified_entities: dict[int, Entity]

    def __init__(self, rom_path: Path) -> None:
        with rom_path.open("rb") as rom:
            self._stream = RomStream(rom.read())

        self._modified_entities = {}
        self._modified_rooms = {}
        self._modified_tilesets = {}

    def get_entity(self, offset: int) -> Entity:
        if offset in self._modified_entities:
            return self._modified_entities[offset]
        entity = Entity(self, offset)
        self._modified_entities[offset] = entity
        return entity

    def get_room(self, offset: int) -> Room:
        if offset in self._modified_rooms:
            return self._modified_rooms[offset]

        room = Room(self, offset)
        self._modified_rooms[offset] = room
        return room

    def get_tileset(self, tileset_type: TilesetType, offset: int) -> Tileset:
        if offset in self._modified_tilesets:
            return self._modified_tilesets[offset]

        tileset = Tileset(self, offset, tileset_type=tileset_type)
        self._modified_tilesets[offset] = tileset
        return tileset
