import threading
from queue import Queue, Empty
from typing import Union, List

from channel.connection import Connection
from net.routing import RoutingTable
from physical.phyconn import PhyConn


class Client:
    routing_table = RoutingTable()
    frame_queue = Queue()
    readers: List[threading.Thread] = list()
    should_stop = threading.Event()

    def __init__(
            self,
            should_stop: threading.Event,
            address: int = None,
            com_l: str = None,
            com_r: str = None,
    ):  # names of serial devices
        self.should_stop = should_stop
        if address:
            if address >= 0b1111_1110:
                raise ValueError(
                    "address is invalid. It should be from 0 to 254 (255 is broadcast)"
                )
            self.address = address
        else:
            self.address = None

        # imagine that every node has virtually 'left' and 'right' connection (i.e. COM-port)
        self.conn_l = (
            Connection(
                self.should_stop,
                PhyConn(self.should_stop, serial_name=com_l),
                src=self.address,
            )
            if com_l
            else None
        )
        self.conn_r = (
            Connection(
                self.should_stop,
                PhyConn(self.should_stop, serial_name=com_r),
                src=self.address,
            )
            if com_l
            else None
        )

        self.connections: List[Connection] = (
            [self.conn_l, self.conn_r] if self.conn_l and self.conn_r else list()
        )

    def set_connections(self, com_l: str, com_r: str):
        self.conn_l = Connection(
            self.should_stop,
            PhyConn(self.should_stop, serial_name=com_l),
            src=self.address,
        )
        self.conn_r = Connection(
            self.should_stop,
            PhyConn(self.should_stop, serial_name=com_r),
            src=self.address,
        )

        self.connections = [
            self.conn_l,
            self.conn_r,
        ]

    def set_address(self, address: int):
        if isinstance(address, str):
            address = int(address)

        if address >= 0b1111_1110:
            raise ValueError(
                "address is invalid. It should be from 0 to 254 (255 is broadcast)"
            )
        self.address = address

    def register(self):
        for conn in self.connections:
            if not conn.is_open:
                conn.open()
        #     frame = conn.recv()  # to handle ack
        #     # possible error handling here
        #     if conn.is_open:
        #         conn.register()
        #         frame = conn.recv()  # to handle reg
        #         if frame.frametype == Frame.TYPE_ERROR:
        #             conn.close()
        #             raise ValueError('address is already taken')
        #         self.add_route(frame.src, conn)

    # def add_route(self, addr, connection):
    #     self.routing_table.add_entry(addr, connection)
    #
    # def remove_route(self, addr):
    #     self.routing_table[addr].close()
    #     self.routing_table.remove_entry(addr)

    def recv_func(self, conn: Connection, stop_event: threading.Event):
        # print(f'[{threading.get_ident()}] RECEIVING FUNC STARTED')
        while True:
            if not stop_event.is_set():
                try:
                    frame = conn.recv()
                except StopIteration:
                    break
                if frame is not None:
                    # print(f'[{threading.get_ident()}] NEW FRAME')
                    self.frame_queue.put_nowait(frame)
            else:
                # print(f'[{threading.get_ident()}] ENDED RECEIVING')
                return

    def start(self):
        """Here we are starting reading threads"""
        for conn in self.connections:
            worker = threading.Thread(
                target=self.recv_func, args=[conn, self.should_stop]
            )
            self.readers.append(worker)
            worker.start()

    def close(self):
        for conn in self.connections:
            conn.close()

    def stop(self):
        for worker in self.readers:
            worker.join()
        self.readers.clear()

    def send(self, data: Union[str, bytes], dst: int):
        # print(f'[{threading.get_ident()}] CLIENT.SEND CALLED')
        for conn in self.connections:
            conn.send(data, dst)

    def read(self):
        while True:
            if not self.should_stop.is_set():
                try:
                    return self.frame_queue.get(timeout=0.5)
                except Empty:
                    continue
            else:
                raise StopIteration
