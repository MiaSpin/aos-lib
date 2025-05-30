
from construct.core import Construct, stream_read, stream_seek, stream_tell
from construct.lib import ListContainer

from aos_lib.structs.common_types import AosPointer
from aos_lib.structs.room import Room


class Area(Construct):
    def _parse(self, stream, context, path):
        room_list_start_offset = int.from_bytes(stream_read(stream, 4, path), 'little') - 0x08000000
        room_list_end_offset = int.from_bytes(stream_read(stream, 4, path), 'little') - 0x08000000
        # seek to beginning of room list for area
        stream_seek(stream, room_list_start_offset, 0, path)

        room_list = []
        while stream_tell(stream, path) != room_list_end_offset:
            room = AosPointer(Room)._parsereport(stream, context, path)
            room_list.append(room)

        return ListContainer(room_list)

