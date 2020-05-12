from datetime import datetime

from PyQt5 import QtCore


class PortListener(QtCore.QObject):
    line = QtCore.pyqtSignal(str)

    def line_recieved(self, text, src):
        content = f"{datetime.now().strftime('%H:%M')} <Собеседник>: {text}"
        self.line.emit(content)
