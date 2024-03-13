from PySide6.QtCore import Qt

from components.mypage import MyPage
from components.layout import MyListView
from components.comment import CommentItem
from models.frontendstates import FrontendStates
from models.dish import DishModel
from models.comment import CommentModel
from qmaterialwidgets import StrongBodyLabel


class CommentPage(MyPage):
    def __init__(
            self, *,
            dish_model: DishModel,
            states: FrontendStates,
            page: MyPage,
            parent=None
    ):
        super(CommentPage, self).__init__(
            object_name='comment-page',
            page_name='评论页',
            states=states,
            prev_page=page,
            parent=parent
        )
        self.states = states
        self.page = page
        self.dish_model = dish_model

        self.title = StrongBodyLabel("全部评论", self)

        self.comment_list = MyListView()
        for comment_uuid in self.dish_model.comments_uuids:
            comment_model = (
                CommentModel()
                .set_states(states=self.states)
                .fetch(uuid=comment_uuid)
            )
            comment_widget = CommentItem(comment_model=comment_model, 
                                         states=self.states, 
                                         page=self.page, 
                                         max_cnt=200, 
                                         height=260)
            self.comment_list.add_widget(comment_widget, comment_model.uuid)
        
        self.init_comment_page()

        
    def init_comment_page(self):
        self.add_widget(self.title, alignment=Qt.AlignLeft)
        self.add_widget(self.comment_list)
        self.add_stretch()

    def update_info(self) -> None: 
        self.comment_list.clear()
        for comment_uuid in self.dish_model.comments_uuids:
            comment_model = (
                CommentModel()
                .set_states(states=self.states)
                .fetch(uuid=comment_uuid)
            )
            comment_widget = CommentItem(comment_model=comment_model,
                                          states=self.states, 
                                          page=self.page, 
                                          max_cnt=200, 
                                          height=300)
            self.comment_list.add_widget(comment_widget, comment_model.uuid)

