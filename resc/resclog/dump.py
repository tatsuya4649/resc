import bitstring
import re


class RescDumpTypeError(TypeError):
    pass


class RescDump:
    def __init__(self, content):
        if not isinstance(content, bytes):
            raise RescDumpTypeError(f"content({content}) \
                must be bytes type.now {type(content)}.")
        self._content = content

    @classmethod
    def bindump(self, content):
        bitarray = bitstring.ConstBitArray(bytes=content)
        binary = bitarray.bin
        splits = re.split(r'(.{8})', binary)[1::2]
        for i in splits:
            bytebit = bitstring.ConstBitArray(f"0b{i}")
            splits[splits.index(i)] = f"{i}({bytebit.bytes})"
        return " ".join(splits)

    @classmethod
    def hexdump(self, content):
        bitarray = bitstring.ConstBitArray(bytes=content)
        return bitarray.hex
