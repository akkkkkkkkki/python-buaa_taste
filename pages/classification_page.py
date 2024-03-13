from typing import Dict, Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from components.dish_item import DishInfoWidget
from components.layout import MonotoneGrid, MyGridView
from components.mylabel import BoldLargeTitleLabel
from components.mypage import MyPage
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.tags import TagsModel
from models.user import UserModel
from pages.detail_page import DetailPage
from pages.show_all_pages import ShowAllDishesPage
from qmaterialwidgets import ElevatedPushButton, TabWidget


class ClassificationPage(MyPage):
    rerender = Signal()

    def __init__(self,
                 states: FrontendStates,
                 user_model: Optional[UserModel],
                 prev_page: Optional[MyPage],
                 parent=None):
        super(ClassificationPage, self).__init__(
            object_name="classification-page",
            page_name="分类页",
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.states = states
        self.user_model = user_model

        self.top_layout = QHBoxLayout()
        self.title_label = BoldLargeTitleLabel('分类')
        self.grid = MonotoneGrid(line_num=4)

        self.init_classification_ui_fun()

    def init_classification_ui_fun(self):
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.add_widget(self.grid)
        self.add_stretch()

        self.grid.setContentsMargins(16, 16, 16, 16)
        self.top_layout.setContentsMargins(32, 0, 16, 16)

    @Slot()
    def update_info(self):
        tags = TagsModel.get_all()

        for tag in tags:
            button = ElevatedPushButton(tag, None)
            button.setFixedWidth(180)

            # noinspection PyUnresolvedReferences
            button.clicked.connect(self.enter(tag))
            self.grid.add_widget(button)

    def click_func(self, dish_model):
        def func():
            self.show_spiner()
            self.push_page(
                DetailPage(
                    dish_model=dish_model,
                    prev_page=self,
                    states=self.states
                )
            )
            self.hide_spiner()

        return func

    def getter(self, tag):
        def func():
            dish_models = DishModel.get_all_dishes(states=self.states)
            new_list = []
            for dish_model in dish_models:
                if tag in dish_model.tags:
                    new_list.append(dish_model)

            return new_list
        return func

    def enter(self, tag):
        def enter_page():
            page = ShowAllDishesPage(
                states=self.states,
                get_list_func=self.getter(tag),
                prev_page=self,
                name=tag
            )
            self.push_page(page)

        return enter_page
