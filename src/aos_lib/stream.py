from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

from aos_lib.structs.rom_object import RomObject

if TYPE_CHECKING:
    from aos_lib.rom import Rom


class RomStream(BytesIO):
    def read_int(self, size: int = 1) -> int:
        """Reads a little endian integer

        param size: number of bytes to read"""
        return int.from_bytes(self.read(size), 'little')

    def read_offset(self) -> int:
        """Reads a 32 bit AoS-styled offset"""
        # the most significant byte of offsets in AoS is always 0x08
        return self.read_int(4) - 0x08000000

    def read_bool(self) -> bool:
        """Reads a bool"""
        return self.read_int() > 0

    def read_array[T: RomObject](
            self,
            rom: Rom,
            element_type: type[T],
            count: int,
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an array of type T with the given length

        param rom: the ROM object the elements belong to
        param count: the length of the array
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        array = []
        for i in range(count):
            array.append(element_type(rom, **element_kwargs))
        return array

    def read_prefixed_array[T: RomObject](
            self,
            rom: Rom,
            element_type: type[T],
            length_size: int,
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an integer of given size, then reads an array of type T of that size

        param rom: the ROM object the elements belong to
        param length_size: the number of bytes to read the array length from
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        length_size = self.read_int(length_size)
        return self.read_array(rom, element_type, length_size, None, **element_kwargs)

    def read_terminated_array[T](
            self,
            rom: Rom,
            element_type: type[T],
            terminator: bytes = b'\x00',
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an array of type T until a terminating value is reached

        param rom: the ROM object the elements belong to
        param terminator: the value at the end of the array
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        array = []
        while self.peek(len(terminator)) != terminator:
            array.append(element_type(rom, **element_kwargs))
        return array

    def read_pointer(self, func: callable, *args, **kwargs):
        """Reads an offset, seeks to it, calls the given function,
        then returns to the original position in the stream

        param func: the function to call after seeking
        *args: positional arguments to pass to the function
        **kwargs: keyword arguments to pass to the function
        returns: the return value of the function"""
        fallback, _ = self.read_and_seek()
        result = func(*args, **kwargs)
        self.seek(fallback)
        return result

    def read_and_seek(self) -> tuple[int, int]:
        """Reads an offset then seeks to it

        returns: position after reading offset, offset read"""
        offset = self.read_offset()
        fallback = self.tell()
        self.seek(offset)
        return (fallback, offset)

    def peek(self, size: int = 1) -> bytes:
        """Reads upcoming bytes without advancing the stream

        param size: number of bytes to read"""
        peeked = self.read(size)
        self.seek(-size, 1)
        return peeked
