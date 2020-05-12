from channel.connection import Connection


class RoutingTable:
    # a dict of "string" reprs of conn (addr) and a Connection objects
    _table = dict()

    def __getitem__(self, key):
        return self._table[key]

    def keys(self):
        return self._table.keys()

    def add_entry(self, address, conn: Connection):
        self._table[address] = conn

    def remove_entry(self, address):
        self._table.pop(address)
