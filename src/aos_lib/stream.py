from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

from aos_lib.structs.rom_object import RomObject

if TYPE_CHECKING:
    pass


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
            element_call: callable,
            count: int,
            *element_args,
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an array of a given size, calling a callalable to create each element

        param rom: the ROM object the elements belong to
        param count: the length of the array
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        array = []
        for i in range(count):
            array.append(element_call(*element_args, **element_kwargs))
        return array

    def read_prefixed_array[T: RomObject](
            self,
            element_call: callable,
            length_size: int,
            *element_args,
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an integer of given size, then reads an array of that size using a callable

        param rom: the ROM object the elements belong to
        param length_size: the number of bytes to read the array length from
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        count = self.read_int(length_size)
        return self.read_array(element_call, count, *element_args, **element_kwargs)

    def read_terminated_array[T](
            self,
            element_call: callable,
            *element_args,
            terminator: bytes = b'\x00',
            offset: int | None = None,
            **element_kwargs
        ) -> list[T]:
        """Reads an array, calling a callalable to create
        each element until a terminating value is reached

        param element_call: the callable used for each element
        param terminator: the value at the end of the array
        param offset: if provided, seek here before reading the array
        **element_kwargs: arguments to pass to the constructor of elements"""
        if offset is not None:
            self.seek(offset)

        array = []
        while self.peek(len(terminator)) != terminator:
            array.append(element_call(*element_args, **element_kwargs))
        return array

    def read_pointer(self, call: callable, *args, **kwargs):
        """Reads an offset, seeks to it, calls the given function,
        then returns to the original position in the stream

        param call: the function to call after seeking
        *args: positional arguments to pass to the function
        **kwargs: keyword arguments to pass to the function
        returns: the return value of the function"""
        fallback, _ = self.read_and_seek()
        result = call(*args, **kwargs)
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
