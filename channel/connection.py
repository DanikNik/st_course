from typing import Union

from bitstring import BitArray

from channel.frame import Frame
from physical.phyconn import PhyConn


class Connection:
    def __init__(self, conn: PhyConn):
        self.conn = conn

    def send(self, data: Union[str, bytes]):
        frame = Frame(Frame.TYPE_DATA, data)
        self.conn.write(frame.bytes())

    def recv(self) -> Frame:
        """This function recieves the full frame and returns it"""
        # at the beginning framebuffer is empty
        byte = int.from_bytes(self._recv(), 'big')
        if byte != Frame.STARTBYTE:
            raise ValueError
        frametype = int.from_bytes(self._recv(), 'big')
        if frametype not in Frame.TYPES:
            raise ValueError
        datalen = int.from_bytes(self._recv(), 'big')
        if datalen > 0:
            data = self._recv(datalen)
            return Frame(frametype, data)
        return Frame(frametype)

    def _recv(self, n=1):
        """This function recieves one octet"""
        return self.conn.recv(n)

    def open(self, to) -> bool:  # to parameter is unclear
        """Initiate conn establishment"""
        # open physical connection to serial port
        self.conn.open()
        # send SYN
        self._send_syn()
        # wait for ACK
        frame = self.recv()
        return frame.frametype != Frame.TYPE_ACK
        # conn is OK

    def close(self):
        """Initiate conn closing"""
        # send FIN
        self._send_fin()
        frame = self.recv()
        # wait for ACK
        if frame.frametype != Frame.TYPE_ACK:
            raise ValueError
        # wait for FIN now
        frame = self.recv()
        if frame.frametype != Frame.TYPE_FIN:
            raise ValueError
        # send ACK
        self._send_ack()
        # and now we are good to close connection
        self.conn.close()

    def _send_syn(self):
        syn_frame = Frame(Frame.TYPE_SYN)
        syn_frame_encoded = encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_ack(self):
        syn_frame = Frame(Frame.TYPE_ACK)
        syn_frame_encoded = encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_fin(self):
        syn_frame = Frame(Frame.TYPE_FIN)
        syn_frame_encoded = encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_err(self):
        syn_frame = Frame(Frame.TYPE_ERROR)
        syn_frame_encoded = encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)


# DUMMY FUNCTION FOR ENCODING
def encode(data: bytes) -> bytes:
    return data
