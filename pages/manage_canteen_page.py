from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout

from components.canteen_counter_info import CanteenCounterInfo
from components.layout import MonotoneGrid
from components.mylabel import BoldTitleLabel
from components.mypage import MyPage
from models import CanteenModel
from models.frontendstates import FrontendStates
from pages.add_canteen_page import AddCanteenPage
from qmaterialwidgets import FilledPushButton, FluentIcon


class ManageCanteenPage(MyPage):
    rerender = Signal()

    def __init__(
            self, *,
            states: FrontendStates,
            prev_page,
            parent=None
    ):
        super(ManageCanteenPage, self).__init__(
            object_name='manage-canteen-page',
            page_name='管理食堂',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.title = BoldTitleLabel('管理食堂')
        self.add_button = FilledPushButton('添加食堂', None, FluentIcon.ADD)
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

        self.add_button.clicked.connect(
            lambda: self.push_page(
                AddCanteenPage(
                    states=states,
                    is_add=True,
                    canteen_model=None,
                    prev_page=self
                )
            )
        )

    def update_info(self):
        self.grid.clear()
        all_canteens_models = CanteenModel.get_all(states=self.states)
        widgets = {}
        for canteen_model in all_canteens_models:
            QApplication.processEvents()
            widget = CanteenCounterInfo(
                model=canteen_model,
                states=self.states,
                page=self
            )
            widget.clicked.connect(
                self.edit_some_canteen(canteen_model)
            )
            QApplication.processEvents()
            self.grid.add_widget(widget)

    def edit_some_canteen(self, canteen_model: CanteenModel):
        def edit_dish():
            page = AddCanteenPage(
                states=self.states,
                canteen_model=canteen_model,
                is_add=False,
                prev_page=self,
                parent=None
            )
            self.push_page(page)

        return edit_dish
