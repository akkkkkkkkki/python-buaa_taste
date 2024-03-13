from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from components.mypage import MyPage
from components.myuser import Register
from models.frontendstates import FrontendStates


class RegisterPage(MyPage):
    def __init__(
            self, *,
            states: FrontendStates,
            prev_page: MyPage,
            parent: QWidget = None
    ):
        super(RegisterPage, self).__init__(
            object_name='register-page',
            page_name='注册账号',
            states=states,
            prev_page=prev_page,
            parent=parent
        )

        self.register_box = Register(parent=self)
        self.set_disable_further_return(True)

        self.init_register_page_ui()
        self.init_register_page_func()

    def init_register_page_ui(self) -> None:
        self.add_stretch()
        self.add_widget(
            self.register_box,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.add_spacing(32)
        self.add_stretch()

    def init_register_page_func(self) -> None:
        self.register_box.set_submit_return_func(self.return_page)
        self.set_disable_further_return(True)

    def return_page(self) -> None:
        self.pop_page()
