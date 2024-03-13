from typing import Optional

from PySide6.QtWidgets import QHBoxLayout

from components.editors import AddOrEditCounter
from components.infobars import create_success_info_bar
from components.mylabel import BoldLargeTitleLabel
from components.mypage import MyPage
from models import CounterModel
from models.frontendstates import FrontendStates
from qmaterialwidgets import FilledPushButton, FluentIcon, MessageBox, TonalPushButton


class AddCounterPage(MyPage):
    def __init__(
            self, *,
            states: FrontendStates,
            counter_model: Optional[CounterModel],
            is_add: bool,
            prev_page: MyPage,
            parent=None
    ):
        super(AddCounterPage, self).__init__(
            object_name='add-dish-page',
            page_name='添加柜台' if is_add else '修改柜台',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        pass
        self.is_add = is_add
        self.counter_model = counter_model
        self.update_outside_func = None

        self.top_layout = QHBoxLayout()
        self.title_label = BoldLargeTitleLabel('添加柜台' if is_add else '编辑柜台')
        self.delete_button = TonalPushButton('删除', None, FluentIcon.DELETE)
        self.submit_button = FilledPushButton('保存', None, FluentIcon.SAVE)

        self.widget = AddOrEditCounter(
            states=self.states,
            page=self,
            counter_model=self.counter_model
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
            '删除柜台',
            f'你确定要删除这个柜台吗？',
            self.get_root()
        )
        if message.exec():
            self.show_spiner()
            self.counter_model.delete()
            self.hide_spiner()
            self.pop_page()
            create_success_info_bar(
                content='删除柜台成功',
                parent=self.get_root()
            )
