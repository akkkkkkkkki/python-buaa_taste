from typing import Callable, Tuple

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)

from components.edit import PasswordEdit
from models.frontendstates import FrontendStates
from qmaterialwidgets import (
    BodyLabel,
    InfoBar,
    InfoBarPosition,
    LineEdit,
    OutlinedPushButton,
    TitleLabel
)
# noinspection PyUnresolvedReferences
from resources import resources


def make_row(
        form_layout: QFormLayout,
        label_text: str,
        is_edit_password: bool
) -> Tuple[
    QLabel,
    QLineEdit | PasswordEdit
]:
    label = BodyLabel(label_text, None)
    label.setObjectName("label")
    label.setAlignment(Qt.AlignCenter)

    if is_edit_password:
        edit = PasswordEdit()
    else:
        edit = LineEdit()
    edit.setObjectName("edit")
    edit.setLabel(label_text)

    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(0, 4, 0, 4)
    layout.setSpacing(50)

    layout.addWidget(edit)

    widget = QWidget()
    widget.setLayout(layout)

    form_layout.addWidget(widget)

    return label, edit


def make_form() -> Tuple[QFormLayout, QWidget]:
    form_layout = QVBoxLayout()
    form_layout.setSpacing(10)
    form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    form_widget = QWidget()
    form_widget.setLayout(form_layout)
    form_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    return form_layout, form_widget


class Login(QWidget):
    def __init__(self,
                 states: FrontendStates,
                 is_register: bool,
                 parent=None):
        super(Login, self).__init__(parent)
        self.register_window = None
        self.states = states
        self.is_register = is_register

        card = QFrame(self)
        self.layout = QVBoxLayout(card)
        self.layout.setSpacing(30)
        card.setFixedSize(500, 500)

        self.title = TitleLabel("注册" if is_register else "登录", None)
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("main_title")

        self.form_layout, self.form_widget = make_form()
        self.form_layout.setContentsMargins(60, 40, 60, 40)
        self.form_layout.setSpacing(30)
        self.layout.addWidget(self.form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        (self.username_label,
         self.username_edit) = make_row(self.form_layout, "用户名", False)
        self.username_check = self.make_check(
            self.username_edit,
            "用户名不能为空",
            lambda: len(self.username_edit.text()) > 0
        )

        (self.password_label,
         self.password_edit) = make_row(self.form_layout, "密码", True)
        if self.is_register:
            self.password_check = self.make_check(
                self.password_edit,
                "密码应大于 8 位",
                lambda: len(self.password_edit.text()) > 8
            )
        else:
            self.password_check = self.make_check(
                self.password_edit,
                "密码不能为空",
                lambda: len(self.password_edit.text()) > 0
            )

        if self.is_register:
            (self.confirm_password_label,
             self.confirm_password_edit) = make_row(self.form_layout, "确认密码 ", True)
            self.confirm_password_check = self.make_check(
                self.confirm_password_edit,
                "两次密码输入不一致",
                lambda: self.confirm_password_edit.text() == self.password_edit.text()
            )

        self.submit_button = OutlinedPushButton('提交', self)
        self.submit_button.setCursor(Qt.PointingHandCursor)
        # self.submit_button.setStyleSheet("border-radius: 20px;")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.submit_button.clicked.connect(self.handle_submit)
        self.form_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        if not self.is_register:
            self.register_label = QLabel("没有账号？")
            self.register_button = OutlinedPushButton('注册', self)
            # self.register_button.setStyleSheet("border-radius: 20px;")
            self.register_button.setCursor(Qt.PointingHandCursor)
            self.register_button.clicked.connect(self.handle_register)
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignRight)
            layout.setSpacing(0)
            layout.addWidget(self.register_label, alignment=Qt.AlignmentFlag.AlignRight)
            layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignRight)
            self.layout.addLayout(layout)

        self.setLayout(self.layout)

        # 应用样式表
        # self.setStyleSheet(style_sheet)  # 应用样式表到窗口

    @Slot()
    def handle_submit(self) -> None:
        submit_func = self.register_func if self.is_register else self.login_func
        all_checked = self.username_check() \
                      and self.password_check() \
                      and (self.confirm_password_check() if self.is_register else True)
        if all_checked:
            submit_func(
                self.username_edit.text(),
                self.password_edit.text()
            )
            self.close()

    @Slot()
    def handle_register(self) -> None:
        self.register_window = Login(
            login_func=None,
            register_func=self.register_func,
            is_register=True
        )
        self.register_window.show()

    def make_check(
            self,
            line_edit: LineEdit,
            alert_text: str,
            pass_predicate: Callable[[], bool]
    ) -> Callable[[], bool]:
        def check() -> bool:
            passed = pass_predicate()
            if not passed:
                line_edit.setError(True)
                self.createErrorInfoBar(alert_text)
            else:
                line_edit.setError(False)
            return passed

        return check

    def createErrorInfoBar(self, str):
        InfoBar.error(
            title='错误',
            content=str,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,  # won't disappear automatically
            parent=self
        )


def test_login_submit(username: str, password: str) -> None:
    print("登录：")
    print(f"用户名：{username}")
    print(f"密码：{password}")


def test_register_submit(username: str, password: str) -> None:
    print("注册：")
    print(f"用户名：{username}")
    print(f"密码：{password}")


def test_login() -> None:
    app = QApplication([])
    window = Login(
        states=None,
        is_register=False,
    )
    window.setWindowTitle("登录")
    window.show()
    app.exec()


if __name__ == "__main__":
    test_login()
