import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("dialog.ui", self)

        self.okButton.clicked.connect(self.accept)


def main():
    app = QApplication(sys.argv)
    dlg = MyDialog()
    dlg.exec()


if __name__ == "__main__":
    main()

