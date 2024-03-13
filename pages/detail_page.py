import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

from components.mypage import MyPage
from components.detail_left import LeftDetail
from components.detail_right import RightDetail
from components.add_items import AddComments
from models.dish import DishModel
from models.frontendstates import FrontendStates


class DetailPage(MyPage):
    def __init__(
            self, *,
            states: FrontendStates,
            dish_model: DishModel,
            prev_page,
            parent=None):
        super(DetailPage, self).__init__(
            object_name='detail-page',
            page_name="详情页",
            states=states,
            prev_page=prev_page,
            parent=parent
        )
        self.dish_model = dish_model
        self.states = states

        self.left = LeftDetail(dish_model=dish_model, states=states)
        self.right = RightDetail(dish_model=dish_model, states=states, page=self)
        self.add_comment = AddComments(states=self.states, dish_model=self.dish_model)

        self.init_detail_ui()

    def init_detail_ui(self):

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(10)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.left)
        self.left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.right)
        self.top_layout.addStretch()
        self.right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.add_comment)

        self.add_layout(self.top_layout)
        # self.add_stretch()
        # self.add_widget(QLabel("test"))
        
        self.add_layout(self.bottom_layout)
        # self.setSizePolicy()

    def update_info(self) -> None:
        self.left.update_info()
        self.right.update_info()