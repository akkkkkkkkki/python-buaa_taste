from PySide6.QtCore import QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication, QHBoxLayout

from components.dish_item import DishInfoWidget
from components.layout import MonotoneGrid
from components.mylabel import BoldLargeTitleLabel
from components.mypage import MyPage
from models.dish import DishModel
from models.frontendstates import FrontendStates
from pages.add_dish_page import AddDishPage
from qmaterialwidgets import FilledPushButton, FluentIcon


class ManageDishPage(MyPage):
    rerender = Signal()

    def __init__(
            self, *,
            states: FrontendStates,
            prev_page,
            parent=None
    ):
        super(ManageDishPage, self).__init__(
            object_name='manage-dish-page',
            page_name='管理菜品',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.threadpool = QThreadPool()

        self.title = BoldLargeTitleLabel('管理菜品')
        self.add_button = FilledPushButton('添加菜品', None, FluentIcon.ADD)
        self.top_area = QHBoxLayout()
        self.top_area.addWidget(self.title)
        self.top_area.addStretch()
        self.top_area.addWidget(self.add_button)
        self.add_layout(self.top_area)
        self.grid = MonotoneGrid()
        self.add_widget(self.grid)
        self.add_stretch()

        self.top_area.setContentsMargins(32, 0, 16, 16)

        self.rerender.connect(self.update_info)
        # noinspection PyUnresolvedReferences
        self.add_button.clicked.connect(
            lambda: self.push_page(
                AddDishPage(
                    states=states,
                    is_add=True,
                    dish_model=None,
                    prev_page=self
                )
            )
        )

    @Slot()
    def update_info(self):
        self.grid.clear()
        all_dishes_models = DishModel.get_all_dishes(states=self.states)
        for dish_model in all_dishes_models:
            QApplication.processEvents()
            widget = DishInfoWidget(
                dish_model=dish_model,
                states=self.states,
                page=self
            )
            widget.clicked.connect(
                self.edit_some_dish(dish_model)
            )
            QApplication.processEvents()
            self.grid.add_widget(widget)

    def edit_some_dish(self, dish_model: DishModel):
        def edit_dish():
            page = AddDishPage(
                states=self.states,
                dish_model=dish_model,
                is_add=False,
                prev_page=self,
                parent=None
            )
            self.push_page(page)

        return edit_dish
