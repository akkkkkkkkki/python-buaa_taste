from typing import Callable

from PySide6.QtCore import Qt

from components.mypage import MyPage
from components.myuser import Login
from models.frontendstates import FrontendStates
from models.user import UserModel
from pages.register_page import RegisterPage


class LoginPage(MyPage):
    def __init__(
            self, *,
            user_model: UserModel,
            states: FrontendStates,
            prev_page: MyPage,
            parent=None
    ):
        super().__init__(
            object_name='login-page',
            page_name='登录账号',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.user_model = user_model
        self.login_box = Login(
            states=states,
            user_model=self.user_model
        )
        self.login_callback = None

        self.init_login_page_ui()
        self.init_login_page_func()

    def init_login_page_ui(self):
        self.add_stretch()
        self.add_widget(self.login_box, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.add_spacing(32)
        self.add_stretch()

    def init_login_page_func(self):
        self.login_box.set_register_enter_func(self.on_click_register_button)
        self.login_box.set_return_func(self.on_click_login_button)

    def set_login_callback(self, func: Callable) -> None:
        self.login_callback = func

    def on_click_register_button(self) -> None:
        register_page = RegisterPage(
            states=self.states,
            prev_page=self
        )
        self.push_page(register_page)

    def on_click_login_button(self) -> None:
        self.login_callback()
        self.pop_page()
