import logging
import sys
import datetime
import threading

from PyQt5 import QtGui, QtCore, QtWidgets

from client.client import Client
from ui.components import window
from ui.connect_dialog import ConnectDialog
from ui.listener import listener


class ChatApp(window.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port_listener = listener
        self.should_stop = threading.Event()
        self.client: Client = Client(should_stop=self.should_stop)
        self.init_handlers()
        self.init_toolbar()
        self.init_listener()
        self.infoDialog = None
        self.statusBar.showMessage(
            "Чтобы установить соединения и начать работу, нажмите Подключиться"
        )

    def init_handlers(self):
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setAutoDefault(True)
        # self.message.returnPressed.connect(self.send_button.click)
        # self.textList.itemDoubleClicked.connect(self.save_dialog)

    def init_toolbar(self):
        self.mExit.triggered.connect(self.close_connection)
        self.mSetting.triggered.connect(self.apply_settings)
        self.mConnect.triggered.connect(self.establish_connections)
        # self.mInfo.triggered.connect(self.create_dialog)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.stop()
        event.accept()

    def close_connection(self):
        self.statusBar.showMessage("Отключение...")
        self.stop()
        print("Connection closed")
        QtWidgets.qApp.quit()

    def stop(self):
        self.client.close()
        self.should_stop.set()
        self.client.stop()

    def get_conn_params(self):
        return ConnectDialog.get_ports_and_address(self)

    def apply_settings(self):
        com1, com2, address, accepted = self.get_conn_params()
        if not accepted:
            return
        self.client.stop()
        self.should_stop.set()
        address = int(address)
        self.client.set_address(address)
        self.client.set_connections(com1, com2)
        self.statusBar.showMessage(f'ADDR: {address} | COM1: {com1} | COM2: {com2}')
        self.should_stop.clear()
        self.port_listener.start(self.client)
        self.client.start()

    def establish_connections(self):
        self.client.register()

    def send_message(self):
        try:
            message = self.message.toPlainText()
            dst = int(self.dst.text())
            if dst < 0b0000_0000 or dst > 0b1111_1111:
                self.show_service("Адрес не может быть таким")
                return
            if len(message) > 0:
                content = f"{datetime.datetime.now().strftime('%H:%M')} <Вы> <{dst}>: {message}"

                self.client.send(message, dst)
                self.show_message(content)

                self.message.clear()
            else:
                self.show_service("Нельзя отправить пустое сообщение")
        except Exception as e:
            logging.exception("Exception")
            self.show_service("Невозможно отправить сообщение")

    def show_service(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        item.setForeground(QtGui.QColor(27, 151, 243))
        self.textList.addItem(item)
        self.textList.scrollToBottom()

    @QtCore.pyqtSlot(str)
    def show_message(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        self.textList.addItem(item)
        self.textList.scrollToBottom()

    def init_listener(self):
        self.port_listener.line.connect(self.show_message)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
