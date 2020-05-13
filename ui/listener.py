import threading
from datetime import datetime

from PyQt5 import QtCore


class PortListener(QtCore.QObject):
    line = QtCore.pyqtSignal(str)
    conn_established = QtCore.pyqtSignal(bool, str)

    def line_recieved(self, text, src):
        if isinstance(text, bytes):
            text = bytes.decode(text, 'utf-8')
        content = f"{datetime.now().strftime('%H:%M')} <{src}>: {text}"
        self.line.emit(content)

    def start(self, client):
        def reading_func(c):
            try:
                while True:
                    frame = c.read()
                    if frame.frametype == frame.TYPE_DATA:
                        self.line_recieved(frame.data, frame.src)
                        # print(f"[{frame.src}] {frame.data}")
            except StopIteration:
                return

        reader = threading.Thread(target=reading_func, args=[client])
        reader.start()


listener = PortListener()
