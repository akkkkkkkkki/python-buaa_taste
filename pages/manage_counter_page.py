from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout

from components.canteen_counter_info import CanteenCounterInfo
from components.layout import MonotoneGrid
from components.mylabel import BoldTitleLabel
from components.mypage import MyPage
from models import CounterModel
from models.frontendstates import FrontendStates
from pages.add_counter_page import AddCounterPage
from qmaterialwidgets import FilledPushButton, FluentIcon


class ManageCounterPage(MyPage):
    rerender = Signal()

    def __init__(
            self, *,
            states: FrontendStates,
            prev_page,
            parent=None
    ):
        super(ManageCounterPage, self).__init__(
            object_name='manage-counter-page',
            page_name='管理柜台',
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.title = BoldTitleLabel('管理柜台')
        self.add_button = FilledPushButton('添加柜台', None, FluentIcon.ADD)
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
                AddCounterPage(
                    states=states,
                    is_add=True,
                    counter_model=None,
                    prev_page=self
                )
            )
        )

    def update_info(self):
        self.grid.clear()
        all_counters_models = CounterModel.get_all(states=self.states)
        for counter_model in all_counters_models:
            QApplication.processEvents()
            widget = CanteenCounterInfo(
                model=counter_model,
                states=self.states,
                page=self
            )
            widget.clicked.connect(
                self.edit_some_counter(counter_model)
            )
            QApplication.processEvents()
            self.grid.add_widget(widget)

    def edit_some_counter(self, counter_model: CounterModel):
        def edit_dish():
            page = AddCounterPage(
                states=self.states,
                counter_model=counter_model,
                is_add=False,
                prev_page=self,
                parent=None
            )
            self.push_page(page)

        return edit_dish
