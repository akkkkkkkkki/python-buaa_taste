from typing import Optional, Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget
)

from backend import (canteen_add, canteen_get_all_ids, canteen_get_by_uuid, canteen_modify, counter_add,
                     counter_get_by_uuid, counter_modify)
from components.dialogs import upload_image
from components.infobars import (
    create_error_info_bar,
    create_success_info_bar,
    create_warning_info_bar,
    create_info_bar
)
from components.star_rating import StarRating
from models.dish import DishModel
from models.comment import CommentModel
from models.frontendstates import FrontendStates
from qmaterialwidgets import (
    ComboBox, FilledLineEdit,
    FilledPushButton,
    FilledTextEdit,
    FluentIcon,
    LineEdit,
    OutlinedPushButton,
    StrongBodyLabel,
    TextEdit,
    TextPushButton
)


def limit_text_length(text_edit, max_length, content):
    if len(text_edit.toPlainText()) > max_length:
        text = text_edit.toPlainText()[:max_length]
        text_edit.setPlainText(text)
        create_warning_info_bar(content, text_edit)


class AddCanteen(QWidget):
    # noinspection PyUnresolvedReferences
    def __init__(self,
                 states: FrontendStates,
                 is_add: bool,
                 origin_canteen_uuid: Optional[str] = None,
                 parent=None):
        super(AddCanteen, self).__init__(parent)
        self.return_func = None
        self.states = states
        self.is_add = is_add
        self.origin_canteen_uuid = origin_canteen_uuid
        self.image_uuid = None

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        self.title = StrongBodyLabel("添加食堂", self)
        self.layout.addWidget(self.title)

        name_edit = LineEdit(self)
        name_edit.setLabel("食堂名称")
        name_edit.setMaxLength(8)

        des_edit = TextEdit(self)
        des_edit.setLabel("描述")
        des_edit.textChanged.connect(
            lambda: limit_text_length(des_edit, 100, "食堂描述最多100字")
        )

        # 如果是编辑，就设定初始值
        if not is_add:
            canteen_info = canteen_get_by_uuid(origin_canteen_uuid)
            origin_name = canteen_info['name']
            origin_description = canteen_info['description']
            name_edit.setText(origin_name)
            des_edit.setText(origin_description)

        self.image_label = QLabel()

        upload_btn = OutlinedPushButton("选择图片", None)
        upload_btn.clicked.connect(lambda: upload_image(self))

        save_btn = FilledPushButton("保存", self, FluentIcon.SAVE)
        save_btn.clicked.connect(
            lambda: self.save(name_edit.text(), des_edit.toPlainText(), self.image_uuid)
        )

        self.layout.addWidget(name_edit, alignment=Qt.AlignLeft)
        self.layout.addWidget(des_edit, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(upload_btn, alignment=Qt.AlignLeft)
        self.layout.addWidget(save_btn, alignment=Qt.AlignRight)

    def save(self, name, des, image_uuid):
        if len(name) < 1 or len(des) < 1:
            if len(name) < 1:
                create_error_info_bar("食堂名称不能为空", self)
            elif len(des) < 1:
                create_error_info_bar("食堂描述不能为空", self)
            return
        # 弹出消息提示
        else:
            image = image_uuid if image_uuid is not None else None
            if self.is_add:
                canteen_add(self.states.user_uuid, name, des, image=image)
                create_success_info_bar(content=f"{name}", parent=self)
                self.return_func()
            else:
                canteen_modify(self.states.user_uuid, self.origin_canteen_uuid, name, des, image=image)
                create_success_info_bar(content=f"{name}", parent=self)
                self.return_func()
                return


class AddCounter(QWidget):
    def __init__(self,
                 is_add: bool,
                 states: FrontendStates,
                 origin_uuid: Optional[str] = None,
                 parent=None):
        super(AddCounter, self).__init__(parent)
        self.return_func = None
        self.is_add = is_add
        self.states = states
        self.origin_uuid = origin_uuid

        self.image = None

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)

        self.title = StrongBodyLabel("添加柜台", self)
        self.layout.addWidget(self.title)

        self.canteen_combo = ComboBox()
        canteens_uuids = canteen_get_all_ids()
        self.canteens = {}
        for canteen_uuid in canteens_uuids:
            canteen_info = canteen_get_by_uuid(canteen_uuid)
            canteen_name = canteen_info['name']
            self.canteen_combo.addItem(canteen_name)
            self.canteens[canteen_name] = canteen_uuid

        name_edit = LineEdit(self)
        name_edit.setLabel("柜台名称")

        name_edit.setMaxLength(10)
        des_edit = TextEdit(self)
        des_edit.setLabel("描述")
        # noinspection PyUnresolvedReferences
        des_edit.textChanged.connect(
            lambda: limit_text_length(des_edit, 100, "柜台描述最多100字")
        )

        # 如果是编辑
        if not is_add:
            origin_counter_info = counter_get_by_uuid(self.origin_uuid)
            origin_canteen_uuid = origin_counter_info['canteen_uuid']
            origin_canteen_info = canteen_get_by_uuid(origin_canteen_uuid)
            origin_canteen_name = origin_canteen_info['name']
            origin_counter_description = origin_counter_info['description']
            name_edit.setText(origin_counter_info['name'])
            des_edit.setText(origin_counter_description)
            self.canteen_combo.setCurrentText(origin_canteen_name)

        self.image_label = QLabel()

        upload_btn = OutlinedPushButton("选择图片", None)
        # noinspection PyUnresolvedReferences
        upload_btn.clicked.connect(lambda: upload_image(self))

        save_btn = FilledPushButton("保存", self, FluentIcon.SAVE)
        # noinspection PyUnresolvedReferences
        save_btn.clicked.connect(
            lambda: self.save(
                self.canteen_combo.currentText(),
                name_edit.text(),
                des_edit.toPlainText(),
                self.image
            )
        )

        self.canteen_combo.setFixedWidth(200)
        self.layout.addWidget(self.canteen_combo)
        self.layout.addWidget(name_edit, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(des_edit, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(upload_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def save(self, canteen, name, des, image):
        if len(name) < 1 or len(des) < 1 or image is None:
            if len(name) < 1:
                create_error_info_bar("柜台名称不能为空", self)
            elif len(des) < 1:
                create_error_info_bar("柜台描述不能为空", self)
            else:
                create_error_info_bar("请上传柜台图片", self)
            return
        # 弹出消息提示
        else:
            if self.is_add:
                counter_add(self.states.user_uuid, name, self.canteens[canteen], des, image)
                create_success_info_bar(content=f"{canteen} {name}", parent=self)
                self.return_func()
            else:
                # counter_modify(self.states.user_uuid, self.canteens[canteen], name, des, image )
                counter_modify(
                    user_uuid=self.states.user_uuid,
                    counter_uuid=self.origin_uuid,
                    name=name,
                    canteen_uuid=self.canteens[canteen],
                    description=des,
                    image=image
                )
                # TODO
                create_success_info_bar(content=f"{canteen} {name}", parent=self)
                self.return_func()


class AddComments(QWidget):
    def __init__(self,
                 dish_model: DishModel,
                 states: FrontendStates,
                 parent=None):
        super(AddComments, self).__init__(parent)
        self.states = states
        self.dish_model = dish_model

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setSpacing(15)

        self.layout.addWidget(StrongBodyLabel("添加你的评论", self), alignment=Qt.AlignLeft)

        title_layout = QHBoxLayout()

        self.title_edit = FilledLineEdit(self)
        self.title_edit.setPlaceholderText("请输入评论标题")
        self.title_edit.setMaxLength(20)
        self.title_edit.setFixedWidth(200)

        title_layout.addWidget(self.title_edit)
        title_layout.addStretch()

        self.content_edit = FilledTextEdit(self)
        self.content_edit.setFixedSize(800, 200)
        # noinspection PyUnresolvedReferences
        self.content_edit.textChanged.connect(
            lambda: limit_text_length(self.content_edit, 200, "评论最多200字")
        )

        self.star_rating = StarRating(0, True, True, False)

        btn_layout = QHBoxLayout()

        clear_btn = TextPushButton("清空", self)
        # noinspection PyUnresolvedReferences
        clear_btn.clicked.connect(self.clear)
        btn_layout.addWidget(clear_btn, alignment=Qt.AlignLeft)
        btn_layout.addStretch()
        submit_btn = OutlinedPushButton("提交", self, FluentIcon.ACCEPT)
        submit_btn.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(submit_btn, alignment=Qt.AlignRight)
        # noinspection PyUnresolvedReferences
        submit_btn.clicked.connect(
            lambda: self.submit(
                self.title_edit.text(),
                self.content_edit.toPlainText()
            )
        )

        self.layout.addLayout(title_layout)
        self.layout.addWidget(self.content_edit, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.star_rating, alignment=Qt.AlignLeft)
        self.layout.addLayout(btn_layout)

        # placeholder_label = QLabel("请输入评论内容")
        # placeholder_label.setStyleSheet("QLabel { color: gray; font-size: 11pt}")
        # placeholder_label.move(15, 15)
        # placeholder_label.setParent(self.content_edit)

        # def handle_text_change():
        #     if self.content_edit.toPlainText().strip():
        #         placeholder_label.hide()
        #     else:
        #         placeholder_label.show()

        # noinspection PyUnresolvedReferences
        # self.content_edit.textChanged.connect(handle_text_change)

    def clear(self):
        self.title_edit.clear()
        self.content_edit.clear()
        self.star_rating.set_rating(1)

    def submit(self, title, content):
        if self.states.is_loggedin:
            if len(title) < 1 or len(content) < 1:
                if len(title) < 1:
                    create_error_info_bar("评论标题不能为空", self)
                else:
                    create_error_info_bar("评论内容不能为空", self)
            else:
                if self.star_rating.get_rating() == 0:
                    create_warning_info_bar("评分不能为0", self)
                else:
                    create_success_info_bar(content=f"成功添加评论：{title}", parent=self)
                    self.dish_model.add_comment(
                        title=title,
                        content=content,
                        rating=self.star_rating.get_rating(),
                        image=None
                    )
                    self.clear()
        else:
            create_info_bar(title="提示", content="请登录后评论", parent=self)

class AddReply(QWidget):
    def __init__(self,
                 dish_model: DishModel,
                 comment_model: CommentModel,
                 states: FrontendStates,
                 on_click_submit_func: Callable,
                 parent=None):
        super(AddReply, self).__init__(parent)
        self.states = states
        self.dish_model = dish_model
        self.comment_model = comment_model
        self.on_click_submit_func = on_click_submit_func

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setSpacing(15)

        self.layout.addWidget(StrongBodyLabel("回复评论", self), alignment=Qt.AlignLeft)

        self.content_edit = FilledTextEdit(self)
        # self.content_edit.setFixedSize(800, 200)
        # noinspection PyUnresolvedReferences
        self.content_edit.textChanged.connect(
            lambda: limit_text_length(self.content_edit, 200, "回复最多200字")
        )

        btn_layout = QHBoxLayout()

        clear_btn = TextPushButton("清空", self)
        # noinspection PyUnresolvedReferences
        clear_btn.clicked.connect(self.clear)
        btn_layout.addWidget(clear_btn, alignment=Qt.AlignLeft)
        btn_layout.addStretch()
        submit_btn = OutlinedPushButton("提交", self, FluentIcon.ACCEPT)
        btn_layout.addWidget(submit_btn, alignment=Qt.AlignRight)
        # noinspection PyUnresolvedReferences
        submit_btn.clicked.connect(
            lambda: self.submit(
                self.content_edit.toPlainText()
            )
        )

        self.layout.addWidget(self.content_edit, alignment=Qt.AlignLeft)
        self.layout.addLayout(btn_layout)

        # placeholder_label = QLabel("请输入回复内容")
        # placeholder_label.setStyleSheet("QLabel { color: gray; font-size: 11pt}")
        # placeholder_label.move(15, 15)
        # placeholder_label.setParent(self.content_edit)

        # def handle_text_change():
        #     if self.content_edit.toPlainText().strip():
        #         placeholder_label.hide()
        #     else:
        #         placeholder_label.show()

        # noinspection PyUnresolvedReferences
        # self.content_edit.textChanged.connect(handle_text_change)

    def clear(self):
        self.content_edit.clear()

    def submit(self, content):
        if len(content) < 1:
            create_error_info_bar("回复内容不能为空", self)
        else:
            self.on_click_submit_func(content)
            create_success_info_bar(content="回复成功", parent=self)
            self.clear()