import sys

from channel.connection import Connection
from physical.phyconn import PhyConn


if __name__ == '__main__':
    phyconn = PhyConn(serial_name=sys.argv[1])