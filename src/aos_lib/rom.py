from pathlib import Path

from aos_lib.stream import RomStream


class Rom:
    _stream: RomStream

    def __init__(self, rom_path: Path) -> None:
        with rom_path.open("rb") as rom:
            self._stream = RomStream(rom.read())
