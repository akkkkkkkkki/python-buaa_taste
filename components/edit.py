from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLineEdit

from components.myicons import MyIcon
from qmaterialwidgets import Action, LineEdit
# noinspection PyUnresolvedReferences
from resources import resources


class PasswordEdit(LineEdit):
    def __init__(self, parent=None):
        super(PasswordEdit, self).__init__(parent)

        self.visible_icon = MyIcon.EYE
        self.hidden_icon = MyIcon.EYEOFF

        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.toggle_password_action = Action(self.hidden_icon, '密码显示/隐藏')
        self.setTrailingAction(self.toggle_password_action)
        self.toggle_password_action.setCheckable(True)
        self.toggle_password_action.setChecked(False)
        # noinspection PyUnresolvedReferences
        self.toggle_password_action.toggled.connect(self.on_toggle_password_action)

    @Slot()
    def on_toggle_password_action(self, show: bool) -> None:
        if show:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(self.visible_icon)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(self.hidden_icon)
