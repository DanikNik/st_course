import time
from typing import Union

from channel.frame import Frame
from channel.hamming import Hamming
from physical.phyconn import PhyConn


class Connection:
    def __init__(self, conn: PhyConn):
        self.conn = conn
        self.is_open = False

        # these parameters mean that the connection
        # waits for ACK for specified action
        self.waiting_open = False
        self.waiting_close = False
        self.waiting_data_ack = False

    def send(self, data: Union[str, bytes]):
        if not self.is_open:
            print('connection is closed')
            return
        frame = Frame(Frame.TYPE_DATA, data)
        self.conn.write(frame.bytes())
        self.waiting_data_ack = True

    def handle_frame(self, frame: Frame):
        print('GOT', frame.frametype_verbose)
        # here we are handling handshake conditions
        if self.waiting_open:
            if frame.frametype == Frame.TYPE_ACK:
                self.is_open = True
                self.waiting_open = False
                return
            raise ValueError
        elif self.waiting_close:
            if frame.frametype == Frame.TYPE_ACK:
                self.is_open = False
                self.waiting_close = False
                return
            raise ValueError
        elif self.waiting_data_ack:
            if frame.frametype == Frame.TYPE_ACK:
                self.waiting_data_ack = False
                return
            raise ValueError

        # if it is a data frame we send ACK frame
        if frame.frametype == Frame.TYPE_DATA:
            self._send_ack()
            return

        if self.is_open:
            # if conn is open, we need to handle FIN frames to close it
            if frame.frametype == Frame.TYPE_FIN:
                self._send_ack()
                self.is_open = False
        else:
            # if conn is not open, we need to handle SYN frames to open it
            if frame.frametype == Frame.TYPE_SYN:
                self._send_ack()
                self.is_open = True

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
            frame = Frame(frametype, data)
        else:
            frame = Frame(frametype)
        self.handle_frame(frame)
        return frame

    def _recv(self, n=1):
        """This function recieves one octet"""
        return self.conn.recv(n)

    def open(self):
        """Initiate conn establishment"""
        # send SYN
        self._send_syn()
        # wait for ACK
        self.waiting_open = True
        # conn is OK

    def close(self):
        """Initiate conn closing"""
        # send FIN
        self._send_fin()
        frame = self.recv()
        # wait for ACK
        self.waiting_close = True

    def _send_syn(self):
        print('SENT SYN')
        syn_frame = Frame(Frame.TYPE_SYN)
        syn_frame_encoded = Hamming.encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_ack(self):
        print('SENT ACK')
        syn_frame = Frame(Frame.TYPE_ACK)
        syn_frame_encoded = Hamming.encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_fin(self):
        print('SENT FIN')
        syn_frame = Frame(Frame.TYPE_FIN)
        syn_frame_encoded = Hamming.encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_err(self):
        print('SENT ERR')
        syn_frame = Frame(Frame.TYPE_ERROR)
        syn_frame_encoded = Hamming.encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)
