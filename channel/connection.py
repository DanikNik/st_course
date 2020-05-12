import threading
from textwrap import wrap
from typing import Union

from bitstring import BitArray

from channel.frame import Frame
from channel.hamming import Hamming
from physical.phyconn import PhyConn


class ConnectionClosedError(ValueError):
    pass


class Connection:
    def __init__(self, conn: PhyConn, src: int = 0, dst: int = 0):
        self.src = src
        self.dst = dst
        self.conn = conn
        self.is_open = False

        # these parameters mean that the connection
        # waits for ACK for specified action
        self.waiting_open = False
        self.waiting_close = False
        self.waiting_data_ack = False
        self.waiting_data_ack_from = 0
        self.waiting_reg = False

    def send(self, data: Union[str, bytes], dst: int):
        # print(f'[{threading.get_ident()}] CONNECTION.SEND CALLED')
        if not self.is_open:
            raise ConnectionClosedError
        frame = Frame(Frame.TYPE_DATA, data, self.src, dst)
        # print(f'[{threading.get_ident()}] FRAME DATA: {frame.dst} {frame.data}')
        try:
            framebytes = frame.bytes()
        except Exception as e:
            return
        self.conn.write(framebytes)
        self.waiting_data_ack = True
        self.waiting_data_ack_from = frame.dst

    def recv(self) -> Union[Frame, None]:
        """This function recieves the full frame and returns it"""
        # at the beginning "framebuffer" is empty
        # print(f'[{threading.get_ident()}] CONNECTION.RECV CALLED')
        byte = int.from_bytes(self._recv(), "big")
        if byte != Frame.STARTBYTE:
            raise ValueError
        frametype = int.from_bytes(self._recv(), "big")
        if frametype not in Frame.TYPES:
            raise ValueError
        src = int.from_bytes(self._recv(), "big")
        dst = int.from_bytes(self._recv(), "big")
        datalen = int.from_bytes(self._recv(), "big")
        if datalen > 0:
            data = self._recv(datalen)
            frame = Frame(frametype, data, src, dst)
        else:
            frame = Frame(frametype, src=src, dst=dst)
        # print(f'[{threading.get_ident()}] RECEIVED {wrap(BitArray(frame.bytes()).bin, 8)}')
        drop_frame = self.handle_frame(frame)
        # print(f'[{threading.get_ident()}] CONNECTION.RECV ENDED')
        if drop_frame:
            return None
        return frame

    def handle_frame(self, frame: Frame):
        # print(f'[{threading.get_ident()}] HANDLING INCOME FRAME')

        # here we are handling handshake conditions
        # actually, this part is about handling responses
        if self.waiting_open:
            if frame.frametype == Frame.TYPE_ACK:
                self.dst = frame.src
                self.is_open = True
                self.waiting_open = False
                print(f"[{frame.src}] INITED CONNECTION")
                return True
            raise ValueError("open")
        elif self.waiting_close:
            if frame.frametype == Frame.TYPE_ACK:
                self.is_open = False
                self.waiting_close = False
                return True
            raise ValueError("close")
        elif self.waiting_data_ack:
            if frame.frametype == Frame.TYPE_ACK:
                self.waiting_data_ack = False
                return True
            elif frame.frametype == Frame.TYPE_NACK:
                self.waiting_data_ack = False
                return True
            raise ValueError("data")
        elif self.waiting_reg:
            if frame.frametype == Frame.TYPE_ACK:
                self.dst = frame.src
                self.waiting_reg = False
                return True
            raise ValueError("reg")

        # this part is about handling requests from remote nodes
        # here we handle registering new node in network
        if frame.frametype == Frame.TYPE_REG:
            if self.src == frame.src:
                self._send_err()
            else:
                self.dst = frame.src
                self._send_ack()
            return True

        # if it is a data frame we send ACK frame...
        elif frame.frametype == Frame.TYPE_DATA:
            if frame.dst == self.src or frame.dst == Frame.BROADCAST:
                # ...only if it is sent to us or broadcast
                self._send_ack()
                return False
            else:
                # if frame's dst doesn't match address, we just reject it
                self._send_nack()
                return True

        if self.is_open:
            # if conn is open, we need to handle FIN frames to close it
            if frame.frametype == Frame.TYPE_FIN:
                self._send_ack()
                self.is_open = False
                return True
        else:
            # if conn is not open, we need to handle SYN frames to open it
            if frame.frametype == Frame.TYPE_SYN:
                self.dst = frame.src
                self._send_ack()
                self.is_open = True
                print(f"[{frame.src}] OPENED CONNECTION")
                return True

    def _recv(self, n=1):
        """This function recieves one octet"""
        return self.conn.recv(n)

    def open(self):
        """Initiate conn establishment"""
        # send SYN
        self._send_syn()
        # wait for ACK
        self.waiting_open = True

    def close(self):
        """Initiate conn closing"""
        # send FIN
        self._send_fin()
        # wait for ACK
        self.waiting_close = True

    def register(self):
        """Register node in network"""
        # send REG
        self._send_reg()
        # wait for ACK
        self.waiting_reg = True

    def _send_service_frame(self, frametype: int):
        syn_frame = Frame(frametype, src=self.src, dst=self.dst)
        syn_frame_encoded = Hamming.encode(syn_frame.bytes())
        self.conn.write(syn_frame_encoded)

    def _send_syn(self):
        self._send_service_frame(Frame.TYPE_SYN)

    def _send_ack(self):
        self._send_service_frame(Frame.TYPE_ACK)
    def _send_nack(self):
            self._send_service_frame(Frame.TYPE_NACK)

    def _send_fin(self):
        self._send_service_frame(Frame.TYPE_FIN)

    def _send_err(self):
        self._send_service_frame(Frame.TYPE_ERROR)

    def _send_reg(self):
        self._send_service_frame(Frame.TYPE_REG)
