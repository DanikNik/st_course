# Frame sructure
# 11111111 - startbyte
# xxxxxxxx - frametype
# xxxxxxxx - datalen (in bytes)
# xxxxxxxx - data (datalen)
#
# If there is no data in frame, then datalen is 0 and data sector of frame is absent
from textwrap import wrap
from typing import Union

from bitstring import BitArray


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


class Frame:
    STARTBYTE = 0b1111_1111

    # CONNECTION MANAGEMENT FRAMETYPES
    TYPE_SYN = 0b0000_0001
    TYPE_FIN = 0b0000_0010
    # APPROVEMENT FRAMETYPES
    TYPE_ACK = 0b0000_0100
    TYPE_ERROR = 0b0000_0101
    # MISC FRAMETYPES
    TYPE_DATA = 0b0000_1000

    def __init__(
            self,
            frametype: int,
            data: Union[bytes, str] = None
    ):
        self.frametype = frametype
        self.datalen = len(data) if data is not None else 0
        self.data = bytes(data, 'utf-8') if isinstance(data, str) else data

    def bytes(self):
        framebytes = bytes([self.STARTBYTE, self.frametype, self.datalen])
        if self.datalen != 0:
            framebytes += self.data
        return framebytes

    @classmethod
    def from_bytes(cls, data: bytes):
        startbyte = data[0]
        if startbyte != Frame.STARTBYTE:
            raise ValueError('startbyte is not a startbyte:)')
        frametype = data[1]
        datalen = data[2]
        if datalen > 0:
            body = data[3:]
            return cls(frametype, body)
        else:
            return cls(frametype)
