import sys
from typing import Dict, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QWidget)

from models.frontendstates import FrontendStates

from qmaterialwidgets import StrongBodyLabel, TonalPushButton, FluentIcon

from components.layout import MyListView
from components.comment import CommentItem
from components.mypage import MyPage
from components.infobars import create_info_bar
from pages.comment_page import CommentPage
from models.comment import CommentModel
from models.dish import DishModel

class RightDetail(QWidget):
    def __init__(self,
                 dish_model: DishModel,
                 page: MyPage,
                 states: FrontendStates = None,
                 parent=None):
        super(RightDetail, self).__init__(parent)
        self.states = states
        self.dish_model = dish_model
        self.page = page

        self.title = StrongBodyLabel("评论", self)
        self.comments = MyListView(limit=3)
        comment_uuids = dish_model.comments_uuids
        self.comment_models = []
        if self.states.is_loggedin:
            for i in range(min(3, len(comment_uuids))):
                comment_model = (
                    CommentModel()
                    .set_states(states=self.states)
                    .fetch(uuid=comment_uuids[i])
                )
                self.comment_models.append(comment_model)
                comment_item = CommentItem(comment_model=comment_model, 
                                        states=self.states, 
                                        page=self.page)
                self.comments.add_widget(comment_item, f"{i}")

        self.expand_btn = TonalPushButton('查看全部', None, FluentIcon.PAGE_RIGHT)
        self.expand_btn.setCursor(Qt.PointingHandCursor)
        
        # self.resize(300, 600)

        self.init_right_detail_ui()
        self.init_right_detail_func()

    def init_right_detail_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(self.comments)
        self.layout.addStretch()
        self.layout.addWidget(self.expand_btn, alignment=Qt.AlignRight)
        # self.setFixedWidth(400)

    def init_right_detail_func(self):
        self.expand_btn.clicked.connect(self.expand_all_comments)

    def update_info(self):
        self.comment_models.clear()
        comment_uuids = self.dish_model.comments_uuids
        self.comments.clear()
        for i in range(min(3, len(comment_uuids))):
            comment_model = (
                CommentModel()
                .set_states(states=self.states)
                .fetch(uuid=comment_uuids[i])
            )
            self.comment_models.append(comment_model)
            comment_item = CommentItem(comment_model=comment_model, states=self.states, page=self.page)
            self.comments.add_widget(comment_item, f"{i}")

            # todo 因为评论对象可能会变，所以必须全部清除再构造？
            # 但是dish可以直接update；reply page的reply也必须重新构造，其他直接update
    
    def expand_all_comments(self):
        if self.states.is_loggedin:
            self.page.push_page(
                CommentPage(
                    dish_model=self.dish_model,
                    states=self.states,
                    page=self.page
                )
            )
        else:
            create_info_bar(title="提示", content="请登录后查看", parent=self)
