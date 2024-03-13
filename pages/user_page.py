from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout)

from components.mylabel import BoldLargeTitleLabel
from components.mypage import MyPage
from components.record_list import RecordView
from components.user_info import UserInfo
from models.frontendstates import FrontendStates
from models.user import UserModel
from pages.login_page import LoginPage
from pages.manage_canteen_page import ManageCanteenPage
from pages.manage_counter_page import ManageCounterPage
from pages.manage_dish_page import ManageDishPage
from qmaterialwidgets import FilledPushButton, TonalPushButton


class UserPage(MyPage):
    def __init__(
            self, *,
            user_model: UserModel,
            states: FrontendStates,
            parent=None
    ):
        super().__init__(
            object_name='user-page',
            page_name='用户中心',
            states=states,
            prev_page=None,
            parent=parent
        )
        self.user_model = user_model

        self.top_layout = QHBoxLayout()
        self.title_label = BoldLargeTitleLabel('用户中心')
        self.user_info_widget = UserInfo(states=states, user_model=self.user_model)
        self.manage_area = QHBoxLayout()
        self.user_func_layout = QHBoxLayout()
        self.manage_canteen_button = TonalPushButton('管理食堂', None)
        self.manage_counter_button = TonalPushButton('管理柜台', None)
        self.manage_dish_button = TonalPushButton('管理菜品', None)
        self.record_widget = RecordView(states=states, at_page=self)
        self.logout_button = FilledPushButton('注销', None)

        self.init_user_page_ui()
        self.init_user_page_func()

    def init_user_page_ui(self):
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.add_stretch()
        self.add_widget(self.user_info_widget)
        self.add_layout(self.manage_area)
        self.manage_area.addStretch()
        self.manage_area.addWidget(self.manage_canteen_button)
        self.manage_area.addWidget(self.manage_counter_button)
        self.manage_area.addWidget(self.manage_dish_button)
        self.manage_area.addStretch()
        self.add_stretch()
        self.user_func_layout.addWidget(
            self.record_widget,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.add_layout(self.user_func_layout)
        self.add_widget(self.logout_button)
        self.add_stretch()

        self.top_layout.setContentsMargins(32, 0, 16, 16)

    # noinspection PyUnresolvedReferences
    def init_user_page_func(self):
        if not self.states.is_loggedin:
            self.jump_to_login_page()

        self.logout_button.clicked.connect(self.on_logout_button_clicked)
        self.manage_canteen_button.clicked.connect(
            self.on_click_manage_canteen
        )
        self.manage_dish_button.clicked.connect(
            self.on_click_manage_dish
        )
        self.manage_counter_button.clicked.connect(
            self.on_click_manage_counter
        )

    def jump_to_login_page(self):
        self.show_spiner()
        login_page = LoginPage(
            user_model=self.user_model,
            states=self.states,
            prev_page=self
        )
        login_page.set_login_callback(self.on_logged_in)
        self.push_page(login_page, disable_return=True)
        self.hide_spiner()

    def on_logged_in(self) -> None:
        self.show_spiner()
        self.states.update_info()
        self.hide_spiner()
        pass

    def on_logout_button_clicked(self) -> None:
        self.states.logout()
        self.jump_to_login_page()

    def on_click_manage_dish(self):
        page = ManageDishPage(
            states=self.states,
            prev_page=self,
            parent=self
        )
        self.push_page(page)
        page.rerender.emit()

    def on_click_manage_canteen(self):
        page = ManageCanteenPage(
            states=self.states,
            prev_page=self,
            parent=self
        )
        self.push_page(page)
        page.rerender.emit()

    def on_click_manage_counter(self):
        page = ManageCounterPage(
            states=self.states,
            prev_page=self,
            parent=self
        )
        self.push_page(page)
        page.rerender.emit()

    def update_info(self) -> None:
        self.record_widget.update_info()
        self.user_info_widget.update_info()
        if self.states.is_loggedin:
            if not self.user_model.is_admin:
                self.manage_dish_button.setHidden(True)
                self.manage_counter_button.setHidden(True)
                self.manage_canteen_button.setHidden(True)
            else:
                self.manage_dish_button.setHidden(False)
                self.manage_canteen_button.setHidden(False)
                self.manage_counter_button.setHidden(False)
            if len(self.user_model.records_uuids) == 0:
                self.record_widget.setHidden(True)
            else:
                self.record_widget.setHidden(False)
