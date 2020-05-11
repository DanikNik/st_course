from channel.connection import Connection


class RoutingTable:
    # a dict of "string" reprs of conn (addr) and a Connection objects
    table = dict()

    def __getitem__(self, key):
        return self.table[key]

    def add_entry(self, address, conn: Connection):
        self.table[address] = conn

    def remove_entry(self, address):
        self.table.pop(address)