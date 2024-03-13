from typing import Callable, final, List

from PySide6.QtWidgets import (
    QApplication, QWidget
)

from components.dish_item import DishInfoWidget
from components.layout import MonotoneGrid
from components.mypage import MyPage
from models.dish import DishModel
from models.frontendstates import FrontendStates
from pages.detail_page import DetailPage


class ShowAllDishesPage(MyPage):
    def __init__(
            self,
            states: FrontendStates,
            get_list_func: Callable,
            name: str,
            prev_page: MyPage,
            parent: QWidget = None):
        super(ShowAllDishesPage, self).__init__(
            object_name='show-all-page',
            page_name=f"全部{name}",
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.get_list_func = get_list_func
        self.grid = MonotoneGrid()
        self.init_show_all_page_ui()

    @final
    def init_show_all_page_ui(self) -> None:
        self.add_widget(self.grid)
        self.add_stretch()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.update_info()

    def update_info(self) -> None:
        dish_models: List[DishModel] = self.get_list_func()
        self.grid.clear()
        for dish_model in dish_models:
            QApplication.processEvents()
            widget = DishInfoWidget(
                dish_model=dish_model,
                states=self.states,
                page=self
            )
            widget.clicked.connect(self.click_func(dish_model=dish_model))
            self.grid.add_widget(widget)

    def click_func(self, dish_model):
        def func():
            # self.show_spiner()
            self.push_page(
                DetailPage(
                    dish_model=dish_model,
                    prev_page=self,
                    states=self.states
                )
            )
            # self.hide_spiner()

        return func
