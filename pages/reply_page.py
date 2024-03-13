import sys
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QApplication)

from components.mypage import MyPage
from components.layout import MyListView
from components.add_items import AddReply
from models.frontendstates import FrontendStates
from models.comment import CommentModel
from models.dish import DishModel
from qmaterialwidgets import StrongBodyLabel

class ReplyPage(MyPage):
    def __init__(self,
                 dish_model: DishModel,
                 comment_model: CommentModel,
                 states: FrontendStates,
                 prev_page=None,
                 parent=None):
        super().__init__(object_name="replypage", 
                                        page_name="评论回复", 
                                        states=states, 
                                        prev_page=None, 
                                        parent=parent)
        self.states = states
        self.comment_model = comment_model
        self.dish_model = dish_model
        
        self.title1 = StrongBodyLabel("评论", self)
        self.dish_title = StrongBodyLabel("相关菜品", self)
        from components.comment import CommentItem
        self.comment_widget = CommentItem(states=states, 
                                          comment_model=self.comment_model, 
                                          max_cnt=200,
                                          height=300,
                                          page=self)
        from components.dish_item import DishInfoWidget
        self.dish_widget = DishInfoWidget(dish_model=dish_model, states=self.states, page=self)
        self.reply_widget = AddReply(dish_model=self.dish_model, states=self.states, 
                                     comment_model=self.comment_model,
                                     on_click_submit_func=lambda content: self.reply(content))
        self.title2 = StrongBodyLabel("全部回复", self)
        self.reply_list = MyListView()
        # self.reply_list.set_spacing()
        
        for reply_uuid in self.comment_model.replies_uuids:
            reply = (
                CommentModel()
                .set_states(states=self.states)
                .fetch(uuid=reply_uuid)
            )
            reply_widget = CommentItem(comment_model=reply, states=self.states, page=self)
            self.reply_list.add_widget(reply_widget, reply_uuid)

        self.init_reply_page_ui()

    def init_reply_page_ui(self):
        # left_layout = QVBoxLayout()
        # left_layout.addWidget(self.title1)
        # left_layout.addWidget(self.comment_widget)
        # left_layout.addWidget(self.reply_widget)
        # left_layout.addWidget(self.dish_title)
        # left_layout.addStretch()
        # left_layout.addWidget(self.dish_widget)

        # right_layout = QVBoxLayout()
        # right_layout.addWidget(self.title2)
        # right_layout.addWidget(self.reply_list)
        # right_layout.addStretch()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)
        left_layout.addWidget(self.title1)
        left_layout.addWidget(self.comment_widget)
        left_layout.addWidget(self.title2)
        left_layout.addWidget(self.reply_list)
        left_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.setSpacing(50)
        right_layout.addWidget(self.dish_title)
        right_layout.addWidget(self.dish_widget)
        right_layout.addWidget(self.reply_widget)
        right_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addLayout(left_layout)
        top_layout.addStretch()
        top_layout.addLayout(right_layout)
        top_layout.addStretch()
        top_layout.addStretch()
        self.add_layout(top_layout)

    def update_info(self):
        self.comment_widget.update_info()
        self.dish_widget.update_info()  # todo
        self.reply_list.clear()
        from components.comment import CommentItem
        for reply_uuid in self.comment_model.replies_uuids:
            reply = (
                CommentModel()
                .set_states(states=self.states)
                .fetch(uuid=reply_uuid)
            )
            reply_widget = CommentItem(comment_model=reply, states=self.states, page=self)
            self.reply_list.add_widget(reply_widget, reply_uuid)

    def reply(self, content):
        self.comment_model.reply(content=content)