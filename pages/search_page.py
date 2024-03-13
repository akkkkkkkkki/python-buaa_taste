from typing import final

from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QWidget
)

from components.dish_item import DishInfoWidget
from components.layout import MonotoneGrid
from components.mylabel import BoldLargeTitleLabel, BoldTitleLabel
from components.mypage import MyPage
from models.dish import DishModel
from models.frontendstates import FrontendStates
from pages.detail_page import DetailPage
from qmaterialwidgets import (
    FilledSearchLineEdit,
    TonalPushButton
)


class SearchPage(MyPage):
    def __init__(self, states: FrontendStates, parent: QWidget = None):
        super(SearchPage, self).__init__(
            object_name='search-page',
            page_name='搜索页',
            states=states,
            prev_page=None,
            parent=parent
        )
        self.title_label = BoldLargeTitleLabel('搜索')
        self.line_edit = FilledSearchLineEdit()
        self.search_button = TonalPushButton('搜索', None)
        self.grid = MonotoneGrid()

        self.top_layout = QHBoxLayout()
        self.search_bar_layout = QHBoxLayout()

        self.init_search_page_ui()
        self.init_search_page_func()

    @final
    def init_search_page_ui(self) -> None:
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.add_layout(self.search_bar_layout)
        self.search_bar_layout.addStretch()
        self.search_bar_layout.addWidget(self.line_edit)
        self.search_bar_layout.addWidget(self.search_button)
        self.search_bar_layout.addStretch()
        self.add_widget(self.grid)
        self.add_stretch()

        self.top_layout.setContentsMargins(32, 0, 16, 16)
        self.search_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.line_edit.setFixedWidth(360)
        self.search_button.setFixedWidth(120)

    # noinspection PyUnresolvedReferences
    def init_search_page_func(self):
        self.search_button.clicked.connect(self.on_click_search_button)

    def on_click_search_button(self):
        widget_models = DishModel.search(
            states=self.states, keyword=self.line_edit.text()
        )
        print(widget_models)
        widgets = [
            DishInfoWidget(
                dish_model=dish_model,
                states=self.states,
                page=self
            ) for dish_model in widget_models
        ]
        self.grid.clear()
        for widget in widgets:
            QApplication.processEvents()
            widget.clicked.connect(self.click_func(widget.dish_model))
            self.grid.add_widget(widget)

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

    def update_info(self) -> None:
        self.grid.clear()
        self.line_edit.clear()
