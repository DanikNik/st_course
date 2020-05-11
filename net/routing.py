class RoutingTable:
    # a dict of "string" reprs of conn (addr) and a pyserial.Serial objects
    table = dict()

    def __getitem__(self, key):
        return self.table[key]