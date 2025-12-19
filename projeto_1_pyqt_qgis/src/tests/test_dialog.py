import pytest
from app import MyDialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

def test_dialog_loads(qtbot):
    dialog = MyDialog()
    qtbot.addWidget(dialog)

    assert dialog.windowTitle() == "Example Dialog"
    assert dialog.label.text() == "Hello, world!"


def test_ok_button_accepts_dialog(qtbot):
    dialog = MyDialog()
    qtbot.addWidget(dialog)

    dialog.show()
    qtbot.mouseClick(dialog.okButton, Qt.MouseButton.LeftButton)

    assert dialog.result() == QDialog.DialogCode.Accepted
