from abc import abstractmethod

from aos_lib.rom import Rom


class RomObject:
    @abstractmethod
    def __init__(self, rom: Rom, offset: int | None = None) -> None:
        self.rom = rom
        self._stream = rom._stream
        if offset is not None:
            self.rom._stream.seek(offset)
