from typing import Union

from channel.frame import Frame
from physical.phyconn import PhyConn


class Connection:
    def __init__(self, conn: PhyConn):
        self.conn = conn
        self.destination = None

    def send(self, data: Union[str, bytes]):
        pass

    def recv(self) -> Union[str, bytes]:
        pass

    def open(self, to) -> bool:  # to parameter is unclear
        """Initiate conn establishment"""
        # open physical connection to serial port
        self.conn.open()
        # send SYN
        self._send_syn()
        # wait for ACK
        data = self.recv()
        frame = Frame.from_bytes(data)
        return frame.frametype != Frame.TYPE_ACK
        # conn is OK

    def close(self):
        """Initiate conn closing"""
        # send FIN
        self._send_fin()
        frame = Frame.from_bytes(self.recv())
        # wait for ACK
        if frame.frametype != Frame.TYPE_ACK:
            raise ValueError
        # wait for FIN now
        frame = Frame.from_bytes(self.recv())
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
