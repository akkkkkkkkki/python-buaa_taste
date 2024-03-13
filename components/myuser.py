from typing import Callable

from PySide6.QtCore import (
    Qt,
    Slot
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget
)

from backend import (UserAlreadyExists, UserNotExist, UserNotFound, WrongPassword)
from components.edit import PasswordEdit
from components.infobars import create_alert
from components.mycard import MyCard
from components.mycolor import MyColor
from models.frontendstates import FrontendStates
from models.user import UserModel
from my_helpers import (
    check_password_strength,
    check_username
)
from qmaterialwidgets import (
    BodyLabel,
    FilledPushButton,
    LineEdit,
    TextPushButton,
    TitleLabel
)


# noinspection DuplicatedCode
class Login(MyCard):
    def __init__(
            self, *,
            user_model: UserModel,
            states: FrontendStates,
            parent: QWidget = None
    ):
        super(Login, self).__init__(
            width=500,
            height=500,
            orientation=Qt.Orientation.Vertical,
            parent=parent
        )
        self.register_return_func = None
        self.return_func = None
        self.user_model = user_model
        self.states = states

        self.title = TitleLabel('航味', self)
        self.subtitle = BodyLabel('航的味道我知道', self)
        self.username_edit = LineEdit()
        self.username_edit.setLabel('用户名')
        self.password_edit = PasswordEdit()
        self.password_edit.setLabel('密码')
        self.register_label = BodyLabel('没有账号？', self)
        self.register_button = TextPushButton('立即注册', self)
        self.submit_button = FilledPushButton('登录', self)

        self.register_layout = QHBoxLayout()

        self.init_login_ui()
        self.init_login_func()

    def init_login_ui(self):
        self.add_widget(self.title, Qt.AlignmentFlag.AlignHCenter)
        self.add_widget(self.subtitle, Qt.AlignmentFlag.AlignHCenter)
        self.add_stretch()
        self.add_widget(self.username_edit, Qt.AlignmentFlag.AlignHCenter)
        self.add_widget(self.password_edit, Qt.AlignmentFlag.AlignHCenter)
        self.add_layout(self.register_layout)
        self.register_layout.addStretch()
        self.register_layout.addWidget(self.register_label)
        self.register_layout.addWidget(self.register_button)
        self.register_layout.addStretch()
        self.add_stretch()
        self.add_widget(self.submit_button, Qt.AlignmentFlag.AlignHCenter)

        self.username_edit.setFixedWidth(300)
        self.password_edit.setFixedWidth(300)

        self.set_padding(0, 64, 0, 64)
        self.set_spacing(0)
        self.register_layout.setContentsMargins(0, 32, 0, 0)
        self.title.setContentsMargins(0, 0, 0, 5)

        self.title.setStyleSheet(f"color: {MyColor.ORANGE400};")

    # noinspection PyUnresolvedReferences
    def init_login_func(self):
        self.register_button.clicked.connect(self.on_click_register_button)
        self.submit_button.clicked.connect(self.on_click_login_button)

    def set_register_enter_func(self, func: Callable) -> None:
        self.register_return_func = func

    def set_return_func(self, func: Callable) -> None:
        self.return_func = func

    @Slot()
    def on_click_register_button(self) -> None:
        if self.register_return_func is not None:
            self.register_return_func()

    @Slot()
    def on_click_login_button(self) -> None:
        if len(self.username_edit.text()) == 0:
            create_alert(
                '用户名不能为空',
                '请检查用户名',
                self.parent()
            )
        elif len(self.password_edit.text()) == 0:
            create_alert(
                '密码不能为空',
                '请检查密码。',
                self.parent()
            )
        else:
            try:
                self.user_model.login(
                    username=self.username_edit.text(),
                    password=self.password_edit.text()
                )
                if self.return_func is not None:
                    self.return_func()
            except UserNotFound:
                create_alert(
                    '登录失败',
                    '用户不存在',
                    self.parent()
                )
            except UserNotExist:
                create_alert(
                    '登录失败',
                    '用户不存在',
                    self.parent()
                )
            except WrongPassword:
                create_alert(
                    '登录失败',
                    '请检查密码。',
                    self.parent()
                )


# noinspection DuplicatedCode
class Register(MyCard):
    def __init__(
            self, *,
            parent: QWidget = None
    ):
        super(Register, self).__init__(
            500,
            500,
            Qt.Orientation.Vertical,
            parent=parent
        )

        self.title = TitleLabel('注册账号', self)
        self.subtitle = BodyLabel('注册账号以使用完整功能', self)
        self.username_edit = LineEdit()
        self.username_edit.setLabel('用户名')
        self.password_edit = PasswordEdit()
        self.password_edit.setLabel('密码')
        self.confirm_password_edit = PasswordEdit()
        self.confirm_password_edit.setLabel('确认密码')
        self.submit_button = FilledPushButton('注册', self)

        self.submit_return_func = None

        self.init_register_ui()
        self.init_register_func()

    def init_register_ui(self):
        self.add_widget(self.title, Qt.AlignmentFlag.AlignHCenter)
        self.add_widget(self.subtitle, Qt.AlignmentFlag.AlignHCenter)
        self.add_stretch()
        self.add_widget(self.username_edit, Qt.AlignmentFlag.AlignHCenter)
        self.add_widget(self.password_edit, Qt.AlignmentFlag.AlignHCenter)
        self.add_widget(self.confirm_password_edit, Qt.AlignmentFlag.AlignHCenter)
        self.add_spacing(16)
        self.add_stretch()
        self.add_widget(self.submit_button, Qt.AlignmentFlag.AlignHCenter)

        self.username_edit.setFixedWidth(300)
        self.password_edit.setFixedWidth(300)
        self.confirm_password_edit.setFixedWidth(300)

        self.set_padding(0, 64, 0, 64)
        self.set_spacing(0)
        self.title.setContentsMargins(0, 0, 0, 5)

    # noinspection PyUnresolvedReferences
    def init_register_func(self):
        self.submit_button.clicked.connect(self.on_click_submit_button)

    def set_submit_return_func(self, func: Callable) -> None:
        self.submit_return_func = func

    def on_click_submit_button(self) -> None:
        everything_ok = True

        username_validity = check_username(self.username_edit.text())
        password_strength = check_password_strength(self.password_edit.text())
        if username_validity is not None:
            create_alert(
                '用户名不合法',
                username_validity,
                self.parent()
            )
            everything_ok = False
        elif password_strength is not None:
            create_alert(
                '密码强度不足',
                password_strength,
                self.parent()
            )
            everything_ok = False
        elif self.password_edit.text() != self.confirm_password_edit.text():
            create_alert(
                '注册失败',
                '两次密码输入不一致。',
                self.parent()
            )
            everything_ok = False

        if everything_ok:
            try:
                UserModel.register(
                    username=self.username_edit.text(),
                    password=self.password_edit.text(),
                    is_admin=True
                )
                self.submit_return_func()
            except UserAlreadyExists:
                create_alert(
                    '注册失败',
                    '用户名已存在。',
                    self.parent()
                )
