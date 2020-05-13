from PyQt5.QtWidgets import QDialog

from ui.components.connect import Ui_Dialog


class ConnectDialog(Ui_Dialog, QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.submit.clicked.connect(self.accept)

    @staticmethod
    def get_ports_and_address(parent=None):
        dialog = ConnectDialog(parent)
        result = dialog.exec_()
        return (
            dialog.com1.text(),
            dialog.com2.text(),
            # dialog.speed.text(),
            dialog.addr.text(),
            result == dialog.accepted
        )
