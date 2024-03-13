from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)

from components.mycard import MyCard
from components.myicons import MyIcon
from components.mylabel import (
    BoldBodyLabel,
    SecondaryLabel
)
from components.mypage import MyPage
from components.star_rating import StarRating
from models.comment import CommentModel
from models.frontendstates import FrontendStates
from models.user import UserModel
from my_helpers import (
    truncate_text
)
from pages.reply_page import ReplyPage
from qmaterialwidgets import (
    BodyLabel,
    FilledToggleToolButton,
    FluentIcon,
    ImageLabel,
    MessageBox, TextPushButton, TransparentToolButton
)
# noinspection PyUnresolvedReferences
from resources import resources


class CommentItem(MyCard):
    def __init__(
            self,
            comment_model: CommentModel,
            states: FrontendStates,
            page: MyPage,
            max_cnt: int = 80,
            height: int= 200,
            width: int = 360,
            parent: QWidget = None
    ):
        # 用户名和评论时间
        super().__init__(
            width,
            height,
            Qt.Orientation.Vertical,
            parent
        )
        self.comment_model: CommentModel = comment_model
        self.states: FrontendStates = states
        self.page = page

        user_model = (
            UserModel()
            .set_states(states=states)
            .fetch(uuid=comment_model.user_uuid)
        )

        self.username_label = BoldBodyLabel(user_model.username)
        self.avatar_label = ImageLabel(user_model.avatar)
        self.time_label = SecondaryLabel(comment_model.time.to_text())
        self.title_label = (BoldBodyLabel(truncate_text(comment_model.title, 16)) 
                            if comment_model.is_main else None)
        self.content_label = BodyLabel(truncate_text(comment_model.content, max_cnt), None)
        self.rating_label = (StarRating(comment_model.rating) 
                             if comment_model.is_main else None)
        self.likes_button = FilledToggleToolButton(MyIcon.LIKE, None)
        self.likes_count_label = BodyLabel(f'{comment_model.like_count}', None)
        self.dislikes_button = FilledToggleToolButton(MyIcon.DISLIKE, None)
        self.dislikes_count_label = BodyLabel(f'{comment_model.dislike_count}', None)
        if self.comment_model.is_main:
            self.replies_button = TextPushButton(f'{len(comment_model.replies_uuids)}', None, FluentIcon.MESSAGE)
        self.delete_button = TransparentToolButton(FluentIcon.DELETE, None)
        self.alert_dialog = None

        self.top_layout = QHBoxLayout()
        self.user_info_layout = QVBoxLayout()
        self.middle_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.init_comment_item_ui()
        self.init_comment_item_functionality()

    def init_comment_item_ui(self) -> None:
        self.add_layout(self.top_layout)
        self.top_layout.addWidget(self.avatar_label)
        self.top_layout.addLayout(self.user_info_layout)
        self.user_info_layout.addStretch()
        self.user_info_layout.addWidget(self.username_label)
        self.user_info_layout.addWidget(self.time_label)
        self.user_info_layout.addStretch()
        self.top_layout.addStretch()
        if self.comment_model.is_main:
            self.top_layout.addWidget(self.rating_label)
        self.add_layout(self.middle_layout)
        if self.comment_model.is_main:
            self.middle_layout.addWidget(self.title_label)
        self.middle_layout.addWidget(self.content_label)
        self.add_stretch()
        self.add_layout(self.bottom_layout)
        self.bottom_layout.addWidget(self.likes_button)
        self.bottom_layout.addWidget(self.likes_count_label)
        self.bottom_layout.addWidget(self.dislikes_button)
        self.bottom_layout.addWidget(self.dislikes_count_label)
        if self.comment_model.is_main:
            self.bottom_layout.addWidget(self.replies_button)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.delete_button)

        self.set_padding(10, 10, 10, 10)
        self.top_layout.setSpacing(0)
        self.user_info_layout.setSpacing(0)
        if self.comment_model.is_main:
            self.title_label.setContentsMargins(0, 4, 0, 0)
        self.avatar_label.setContentsMargins(0, 0, 10, 0)
        self.username_label.setContentsMargins(0, 0, 0, 2)
        self.likes_button.setFixedSize(32, 32)
        self.dislikes_button.setFixedSize(32, 32)
        if self.comment_model.is_main:
            self.replies_button.setFixedHeight(32)
        self.delete_button.setFixedSize(32, 32)
        self.bottom_layout.setSpacing(10)
        self.set_spacing(0)

        self.avatar_label.setFixedSize(42, 42)
        self.content_label.setWordWrap(True)

    # noinspection PyUnresolvedReferences
    def init_comment_item_functionality(self) -> None:
        self.likes_button.setChecked(self.comment_model.liked)
        self.dislikes_button.setChecked(self.comment_model.disliked)
        self.delete_button.setEnabled(True)

        self.likes_button.toggled.connect(self.on_toggle_likes_button)
        self.dislikes_button.toggled.connect(self.on_toggle_dislikes_button)
        if self.comment_model.is_main:
            self.replies_button.clicked.connect(self.on_click_replies_button)
        self.delete_button.clicked.connect(self.on_click_delete_button)

    # noinspection DuplicatedCode
    def on_toggle_likes_button(self) -> None:
        if self.likes_button.isChecked():
            self.comment_model.like()
        else:
            self.comment_model.cancel_like()
        self.update_info()

    # noinspection DuplicatedCode
    def on_toggle_dislikes_button(self) -> None:
        if self.dislikes_button.isChecked():
            self.comment_model.dislike()
        else:
            self.comment_model.cancel_like()
        self.update_info()

    def on_click_replies_button(self) -> None:
        if self.comment_model.is_main:
            print(self.replies_button.text() + ' 条回复')

    def on_click_delete_button(self) -> None:
        self.alert_dialog = MessageBox(
            '确定删除这条',
            '操作不可恢复。',
            parent=self.parent()
        )
        if self.alert_dialog.exec():
            self.comment_model.delete()

    def update_info(self):
        user_model = (
            UserModel()
            .set_states(states=self.states)
            .fetch(uuid=self.comment_model.user_uuid)
        )

        self.username_label.setText(user_model.username)
        self.time_label.setText(self.comment_model.time.to_text())
        if self.comment_model.is_main:
            self.title_label.setText(self.comment_model.title)
        self.content_label.setText(self.comment_model.content)
        if self.comment_model.is_main:
            self.rating_label = StarRating(self.comment_model.rating)
        self.likes_button.setChecked(self.comment_model.liked)
        self.likes_count_label.setText(f'{self.comment_model.like_count}')
        self.dislikes_button.setChecked(self.comment_model.disliked)
        self.dislikes_count_label.setText(f'{self.comment_model.dislike_count}')
        if self.comment_model.is_main:
            self.replies_button.setText(f'{len(self.comment_model.replies_uuids)}')

    def on_click(self) -> None:
        if self.comment_model.is_main:
            super(CommentItem, self).on_click()
            self.page.push_page(
                ReplyPage(
                    states=self.states,
                    comment_model=self.comment_model,
                    prev_page=self.page,
                    dish_model=self.page.dish_model
                )
            )
