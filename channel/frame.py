# Frame sructure
# 11111111 - startbyte - 1 octet
# xxxxxxxx - frametype - 1 octet
# xxxxxxxx - src - 1 octet (integer number from 1 to 3 actually, but can be anything up to 1 byte)
# xxxxxxxx - dst - 1 octet (integer number from 1 to 3 actually, but can be anything up to 1 byte)
# xxxxxxxx - datalen - 1 octet (in bytes)
# xxxxxxxx - data - $datalen octets (datalen)
#
# If there is no data in frame, then datalen is 0 and data sector of frame is absent
#
# Broadcast address is equivalent to 11111111 (like in TCP/IP)
#
#
#
from typing import Union


class Frame:
    STARTBYTE = 0b1111_1111
    BROADCAST = 0b1111_1111

    # ARP-LIKE FRAMETYPES
    TYPE_REG = 0b1000_0000  # to register node in network

    # CONNECTION MANAGEMENT FRAMETYPES
    TYPE_SYN = 0b0000_0001  # open connection
    TYPE_FIN = 0b0000_0010  # close connection

    # APPROVEMENT FRAMETYPES
    TYPE_ACK = 0b0000_0100  # OK
    TYPE_NACK = 0b0000_0110  # FRAME REJECTION
    TYPE_ERROR = 0b0000_0101  # !OK

    # DATA FRAMETYPE
    TYPE_DATA = 0b0000_1000

    TYPES = [
        # TYPE_REG,
        TYPE_SYN,
        TYPE_FIN,
        TYPE_ACK,
        TYPE_NACK,
        TYPE_ERROR,
        TYPE_DATA,
    ]

    TYPES_VERBOSE = {
        TYPE_SYN: "SYN",
        TYPE_ACK: "ACK",
        TYPE_FIN: "FIN",
        TYPE_ERROR: "ERROR",
        TYPE_DATA: "DATA",
        TYPE_NACK: "NACK",
    }

    def __init__(
            self,
            frametype: int,
            data: Union[bytes, str] = None,
            src: int = None,
            dst: int = None,
    ):
        self.frametype = frametype
        self.frametype_verbose = Frame.TYPES_VERBOSE[frametype]
        self.src = src
        self.dst = dst
        self.datalen = len(data) if data is not None else 0
        self.data = bytes(data, "utf-8") if isinstance(data, str) else data

    def bytes(self):
        framebytes = bytes(
            [self.STARTBYTE, self.frametype, self.src, self.dst, self.datalen]
        )
        if self.datalen != 0:
            framebytes += self.data
        return framebytes

    @classmethod
    def from_bytes(cls, data: bytes):
        startbyte = data[0]
        if startbyte != Frame.STARTBYTE:
            raise ValueError("startbyte is not a startbyte:)")
        frametype = data[1]
        src = data[2]
        dst = data[3]
        datalen = data[4]
        if datalen > 0:
            body = data[5:]
            return cls(frametype, body, src, dst)
        else:
            return cls(frametype, src=src, dst=dst)
