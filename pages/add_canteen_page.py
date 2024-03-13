from typing import Optional

from PySide6.QtWidgets import QHBoxLayout

from components.editors import AddOrEditCanteen
from components.infobars import create_success_info_bar
from components.mylabel import BoldLargeTitleLabel
from components.mypage import MyPage
from models import CanteenModel
from models.frontendstates import FrontendStates
from qmaterialwidgets import FilledPushButton, FluentIcon, MessageBox, TonalPushButton


class AddCanteenPage(MyPage):
    def __init__(
            self, *,
            states: FrontendStates,
            canteen_model: Optional[CanteenModel],
            is_add: bool,
            prev_page: MyPage,
            parent=None
    ):
        super(AddCanteenPage, self).__init__(
            object_name='add-dish-page',
            page_name='添加食堂' if is_add else '修改食堂',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        pass
        self.is_add = is_add
        self.canteen_model = canteen_model
        self.update_outside_func = None

        self.top_layout = QHBoxLayout()
        self.title_label = BoldLargeTitleLabel('添加食堂' if is_add else '编辑食堂')
        self.delete_button = TonalPushButton('删除', None, FluentIcon.DELETE)
        self.submit_button = FilledPushButton('保存', None, FluentIcon.SAVE)

        self.widget = AddOrEditCanteen(
            states=self.states,
            page=self,
            canteen_model=self.canteen_model
        )
        self.init_add_dish_page_ui()
        self.init_add_dish_page_func()

    def init_add_dish_page_ui(self):
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.delete_button)
        self.top_layout.addWidget(self.submit_button)
        self.add_widget(self.widget)
        self.add_stretch()

        self.top_layout.setContentsMargins(32, 0, 16, 16)
        if self.is_add:
            self.delete_button.setHidden(True)

    # noinspection PyUnresolvedReferences
    def init_add_dish_page_func(self):
        self.submit_button.clicked.connect(
            self.widget.save_content
        )
        self.delete_button.clicked.connect(
            self.delete_dish
        )

    def delete_dish(self):
        message = MessageBox(
            '删除食堂',
            f'你确定要删除这个食堂吗？',
            self.get_root()
        )
        if message.exec():
            self.show_spiner()
            self.canteen_model.delete()
            self.hide_spiner()
            self.pop_page()
            create_success_info_bar(
                content='删除食堂成功',
                parent=self.get_root()
            )
