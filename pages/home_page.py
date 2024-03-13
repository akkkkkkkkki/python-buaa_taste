from typing import List, Optional, Tuple

from PySide6.QtCore import Qt, QThreadPool, Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLayout, QPushButton, QVBoxLayout, QWidget

from components.dish_item import DishInfoWidget
from components.layout import MonotoneGrid
from components.mylabel import BoldLargeTitleLabel, BoldTitleLabel
from components.mypage import MyPage
from generator import generate_dish_item
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.user import UserModel
from pages.detail_page import DetailPage
from pages.show_all_pages import ShowAllDishesPage
from qmaterialwidgets import FluentIcon, ScrollArea, TonalPushButton


def make_section(title: str) -> Tuple[QLabel, QPushButton, MonotoneGrid, QLayout, ScrollArea]:
    label = BoldTitleLabel(title)
    button = TonalPushButton('查看全部', None, FluentIcon.PAGE_RIGHT)
    grid = MonotoneGrid(orientation=Qt.Orientation.Horizontal, limit=10)
    scroll_area = ScrollArea()

    main_layout = QVBoxLayout()
    top_layout = QHBoxLayout()

    top_layout.addWidget(label)
    top_layout.addStretch()
    top_layout.addWidget(button)
    main_layout.addLayout(top_layout)
    scroll_area.setWidget(grid)
    main_layout.addWidget(scroll_area)

    scroll_area.setFixedHeight(230)
    scroll_area.setWidgetResizable(True)
    top_layout.setContentsMargins(16, 0, 16, 0)
    main_layout.setContentsMargins(16, 0, 0, 16)
    grid.setContentsMargins(16, 0, 0, 0)

    return label, button, grid, main_layout, scroll_area


class HomePage(MyPage):
    rerender = Signal()

    def __init__(
            self, *,
            states: FrontendStates,
            user_model: Optional[UserModel],
            parent: QWidget = None
    ):
        super().__init__(
            object_name='home-page',
            page_name='主页',
            states=states,
            prev_page=None,
            parent=parent)
        self.thread_pool = QThreadPool()
        self.states: FrontendStates = states
        self.user_model: Optional[UserModel] = user_model

        self.title_label = BoldLargeTitleLabel('首页')
        self.top_layout = QHBoxLayout()
        (self.recommend_label,
         self.recommend_button,
         self.recommend_grid,
         self.recommend_layout,
         self.recommend_scroll) = make_section('为你推荐')
        (self.favorites_label,
         self.favorites_button,
         self.favorites_grid,
         self.favorites_layout,
         self.favorites_scroll) = make_section('我的收藏')
        (self.top_rates_label,
         self.top_rated_button,
         self.top_rated_grid,
         self.top_rated_layout,
         self.top_rated_scroll) = make_section('倍受好评')
        (self.most_pop_label,
         self.most_pop_button,
         self.most_pop_grid,
         self.most_pop_layout,
         self.most_pop_scroll) = make_section('热门菜品')

        self.init_home_page_ui()
        self.init_home_page_func()

    def init_home_page_ui(self) -> None:
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.add_layout(self.recommend_layout)
        self.add_layout(self.favorites_layout)
        self.add_layout(self.top_rated_layout)
        self.add_layout(self.most_pop_layout)
        self.add_stretch()

        self.top_layout.setContentsMargins(32, 0, 16, 16)

    def init_home_page_func(self):
        self.rerender.connect(self.update_info)
        self.recommend_button.clicked.connect(
            lambda: self.push_page(
                ShowAllDishesPage(
                    states=self.states,
                    get_list_func=self.get_recommend_dishes_models,
                    prev_page=self,
                    name="推荐菜品"
                )
            )
        )
        self.favorites_button.clicked.connect(
            lambda: self.push_page(
                ShowAllDishesPage(
                    states=self.states,
                    get_list_func=self.get_recommend_dishes_models,
                    prev_page=self,
                    name="收藏菜品"
                )
            )
        )
        self.top_rated_button.clicked.connect(
            lambda: self.push_page(
                ShowAllDishesPage(
                    states=self.states,
                    get_list_func=self.get_top_rated_dishes_models,
                    prev_page=self,
                    name="高分菜品"
                )
            )
        )
        self.most_pop_button.clicked.connect(
            lambda: self.push_page(
                ShowAllDishesPage(
                    states=self.states,
                    get_list_func=self.get_most_pop_dishes_models,
                    prev_page=self,
                    name="热门菜品"
                )
            )
        )

    def update_info(self) -> None:
        self.recommend_grid.clear()
        self.favorites_grid.clear()
        self.top_rated_grid.clear()
        self.most_pop_grid.clear()
        if self.states.is_loggedin:
            self.user_model.set_states(states=self.states)
            recommend_dishes_models = self.get_recommend_dishes_models()
            self.create_widgets(
                dish_models=recommend_dishes_models,
                grid=self.recommend_grid
            )
            favorite_dishes_models = self.get_favorite_dishes_models()
            self.create_widgets(
                dish_models=favorite_dishes_models,
                grid=self.favorites_grid
            )
            self.set_section_hidden(False)
        else:
            self.set_section_hidden(True)
        top_rated_dishes_models = DishModel.get_top_rated(states=self.states)
        self.create_widgets(
            dish_models=top_rated_dishes_models,
            grid=self.top_rated_grid
        )
        most_pop_dishes_models = DishModel.get_most_popular(states=self.states)
        self.create_widgets(
            dish_models=most_pop_dishes_models,
            grid=self.most_pop_grid
        )

    def get_favorite_dishes_models(self):
        favorite_dishes_models = []
        user_model = (
            UserModel()
            .set_states(states=self.states)
            .fetch(uuid=self.states.user_uuid)
        )
        for dish_uuid in user_model.favorite_dishes_uuids:
            QApplication.processEvents()
            dish_model = (
                DishModel()
                .set_states(states=self.states)
                .fetch(uuid=dish_uuid)
            )
            favorite_dishes_models.append(dish_model)
        return favorite_dishes_models

    def get_recommend_dishes_models(self):
        recommend_dishes_models = []
        user_model = (
            UserModel()
            .set_states(states=self.states)
            .fetch(uuid=self.states.user_uuid)
        )
        for dish_uuid in user_model.recommend_dishes_uuids:
            QApplication.processEvents()
            dish_model = (
                DishModel()
                .set_states(states=self.states)
                .fetch(uuid=dish_uuid)
            )
            recommend_dishes_models.append(dish_model)
        return recommend_dishes_models

    def get_top_rated_dishes_models(self):
        return DishModel.get_top_rated(states=self.states)

    def get_most_pop_dishes_models(self):
        return DishModel.get_most_popular(states=self.states)

    def create_widgets(
            self, *,
            dish_models: List[DishModel],
            grid: MonotoneGrid
    ) -> None:
        for dish_model in dish_models:
            QApplication.processEvents()
            widget = DishInfoWidget(
                dish_model=dish_model,
                states=self.states,
                page=self
            )
            widget.clicked.connect(self.click_func(dish_model))
            QApplication.processEvents()
            grid.add_widget(widget)

    def set_section_hidden(self, hide: bool) -> None:
        if hide or len(self.user_model.recommend_dishes_uuids) == 0:
            self.recommend_label.setHidden(True)
            self.recommend_grid.setHidden(True)
            self.recommend_button.setHidden(True)
            self.recommend_scroll.setHidden(True)
        else:
            self.recommend_label.setHidden(False)
            self.recommend_grid.setHidden(False)
            self.recommend_button.setHidden(False)
            self.recommend_scroll.setHidden(False)
        if hide or len(self.user_model.favorite_dishes_uuids) == 0:
            self.favorites_grid.setHidden(True)
            self.favorites_label.setHidden(True)
            self.favorites_button.setHidden(True)
            self.favorites_scroll.setHidden(True)
        else:
            self.favorites_grid.setHidden(False)
            self.favorites_label.setHidden(False)
            self.favorites_button.setHidden(False)
            self.favorites_scroll.setHidden(False)

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
