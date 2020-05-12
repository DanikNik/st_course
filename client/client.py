import threading
from queue import Queue
from typing import Union, List

from channel.connection import Connection
from channel.frame import Frame
from net.routing import RoutingTable
from physical.phyconn import PhyConn


class Client:
    routing_table = RoutingTable()
    addresses = list()
    frame_queue = Queue()
    readers: List[threading.Thread] = []
    should_stop = threading.Event()

    def __init__(self, address: int, com_l: str, com_r: str):  # names of serial devices
        if address >= 0b1111_1111:
            raise ValueError('address is invalid. It should be from 0 to 254 (255 is broadcast)')
        self.address = address

        # imagine that every node has virtually 'left' and 'right' connection (i.e. COM-port)
        self.conn_l = Connection(PhyConn(serial_name=com_l), src=self.address)
        # self.conn_r = Connection(PhyConn(serial_name=com_r), src=self.address)

        self.connections = [
            self.conn_l,
            # self.conn_r
        ]

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

    def recv_func(self, conn, stop_event: threading.Event):
        print(f'[{threading.get_ident()}] RECEIVING FUNC STARTED')
        while True:
            if not stop_event.is_set():
                frame = conn.recv()
                if frame is not None:
                    print(f'[{threading.get_ident()}] NEW FRAME')
                    self.frame_queue.put_nowait(frame)
            else:
                print(f'[{threading.get_ident()}] ENDED RECEIVING')
                return

    def run(self):
        """Here we are starting reading threads"""
        self.should_stop.clear()
        for conn in self.connections:
            worker = threading.Thread(target=self.recv_func, args=[conn, self.should_stop])
            self.readers.append(worker)
            worker.start()

    def stop(self):
        self.should_stop.set()
        for worker in self.readers:
            worker.join()

    def send(self, data: Union[str, bytes], dst: int):
        print(f'[{threading.get_ident()}] CLIENT.SEND CALLED')
        for conn in self.connections:
            conn.send(data, dst)

    def read(self):
        return self.frame_queue.get()
