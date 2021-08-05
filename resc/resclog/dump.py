import bitstring
import re


class RescDumpTypeError(TypeError):
    pass


class RescDump:
    def __init__(self, content):
        self._content_type(content)
        self._content = content

    @classmethod
    def _content_type(self,content):
        if not isinstance(content, bytes):
            raise RescDumpTypeError(f"content({content}) \
                must be bytes type.now {type(content)}.")
    @classmethod
    def bindump(
        self,
        content,
        ascii=False,
        empty=True,
    ):
        self._content_type(content)
        bitarray = bitstring.ConstBitArray(bytes=content)
        binary = bitarray.bin
        splits = re.split(r'(.{8})', binary)[1::2]
        for i in splits:
            bytebit = bitstring.ConstBitArray(f"0b{i}")
            if ascii:
                splits[splits.index(i)] = f"{i}({bytebit.bytes})"
            else:
                splits[splits.index(i)] = f"{i}"
        gap_str = " " if empty else ""
        return gap_str.join(splits)

    @classmethod
    def hexdump(self, content):
        self._content_type(content)
        bitarray = bitstring.ConstBitArray(bytes=content)
        return bitarray.hex
