from time import time

from PySide6.QtCore import QDate, QSize, Qt, QTime
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget)

from components.rating_count import RatingCount
from components.infobars import create_info_bar, create_success_info_bar
from models.canteen import CanteenModel
from models.counter import CounterModel
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.image import ImageModel
from models.user import UserModel
from my_helpers import crop_scale, load_icon
from qmaterialwidgets import (CalendarPicker, FilledToggleToolButton, FluentIcon, ImageLabel, InfoBar, InfoBarPosition,
                              OutlinedPushButton, TimePicker)
from qmaterialwidgets import BodyLabel, CaptionLabel, ImageLabel, LargeTitleLabel, ScrollArea, \
    StrongBodyLabel, \
    SubtitleLabel, \
    TitleLabel

def normalize(date: QDate, time: QTime):
    year = date.year()
    month = date.month()
    day = date.day()

    hour = time.hour()
    minute = time.minute()

    # 格式化日期和时间为指定格式
    formatted_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
    formatted_time = "{:02d}:{:02d}".format(hour, minute)

    # 拼接日期和时间字符串
    normalized_string = formatted_date + " " + formatted_time

    return normalized_string


class LeftDetail(QWidget):
    def __init__(
            self, *,
            dish_model: DishModel,
            states: FrontendStates = None,
            parent=None
    ):
        super(LeftDetail, self).__init__(parent)
        self.states = states
        self.dish_model = dish_model

        # 初始化时钟
        self.date = QDate()
        self.time = QTime()
        self.add_eat = QWidget()
        self.add_eat.datepicker = CalendarPicker(self.add_eat)
        self.add_eat.timepicker = TimePicker(self.add_eat)
        self.add_eat.save_btn = OutlinedPushButton('保存', self)

        # 初始化保存按钮
        self.save_able = False
        self.time_flag = False
        self.date_flag = False

        # 所有的组件
        self.rating_count = RatingCount(self.dish_model.ratings)
        self.minute_label = CaptionLabel("分")
        self.name_label = LargeTitleLabel(self.dish_model.name)
        self.tags_label = CaptionLabel("|".join(self.dish_model.tags))
        self.counters = []
        for counter_uuid in self.dish_model.counters_uuids:
            counter_model = (
                CounterModel()
                .set_states(states=self.states)
                .fetch(uuid=counter_uuid)
            )
            canteen_model = (
                CanteenModel()
                .set_states(states=states)
                .fetch(uuid=counter_model.canteen_uuid)
            )
            self.counters.append(f"{canteen_model.name}{counter_model.name}")
        self.counter_label = BodyLabel(" | ".join(self.counters))

        self.star_btn = FilledToggleToolButton(FluentIcon.HEART, self)
        self.star_btn.setCursor(Qt.PointingHandCursor)
        self.star_btn.setChecked(False)
        self.rating_label = TitleLabel(str(self.dish_model.rating_average))

        image_model = (
            ImageModel()
            .set_states(states=self.states)
            .fetch(uuid=self.dish_model.image_uuid)
        )
        self.img_label = ImageLabel(crop_scale(image_model.to_image(), 80, 80))
        self.add_eat_btn = QPushButton()
        self.add_eat_btn.setIcon(load_icon("eaten"))
        self.price_label = TitleLabel(f"￥{self.dish_model.price}")
        self.des_title = StrongBodyLabel("描述")
        self.des_label = BodyLabel(self.dish_model.description)

        if self.states.is_loggedin:
            user_model = (
                UserModel()
                .set_states(states=self.states)
                .fetch(uuid=self.states.user_uuid)
            )
            if user_model.check_favorite(dish_uuid=self.dish_model.uuid):
                self.star_btn.setChecked(True)
            self.add_eat_btn.setIcon(load_icon("eaten")
                                    if user_model.check_record(dish_uuid=self.dish_model.uuid) 
                                    else load_icon("addeat"))
   
        self.init_detail_ui()
        self.init_detail_func()

    def init_detail_ui(self):
        # self.top_card.setFixedSize(500, 800)
        self.top_layout = QVBoxLayout(self)
        self.top_layout.setAlignment(Qt.AlignCenter)
        self.top_layout.setSpacing(10)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        ne_card = QFrame()
        row00 = QVBoxLayout(ne_card)
        ne_card.setLayout(row00)
        row00.setAlignment(Qt.AlignLeft)
        row00.addWidget(self.name_label)
        row00.addWidget(self.tags_label)
        row00.addWidget(self.counter_label)

        row0 = QHBoxLayout()

        row0.addWidget(ne_card)
        row0.addStretch()
        row0.addWidget(self.rating_count)
        
        self.rating_label.setAlignment(Qt.AlignBottom)
        
        self.minute_label.setAlignment(Qt.AlignBottom)

        row1 = QHBoxLayout()
        row1.setAlignment(Qt.AlignBottom)
        row1.addWidget(self.star_btn)
        row1.addStretch()
        row1.addWidget(self.rating_label)
        row1.addWidget(self.minute_label)
        row1.setSpacing(0)

        # 菜品图片
        self.img_label.setScaledContents(True)  # 保持图片质量
        self.img_label.setFixedSize(200, 200)
        self.img_label.setAlignment(Qt.AlignCenter)

        # 已吃按钮
        self.add_eat_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 设置按钮背景透明 */
                border: none;  /* 移除按钮边框 */
            }
        """)
        self.add_eat_btn.setFixedSize(40, 40)  # 设置按钮固定尺寸
        self.add_eat_btn.setCursor(Qt.PointingHandCursor)
        self.add_eat_btn.setIconSize(QSize(40, 40))
        # noinspection PyUnresolvedReferences
        self.add_eat_btn.clicked.connect(self.show_picker)
        

        row3 = QHBoxLayout()
        # 创建一个占位部件并将其加入布局中
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        row3.addWidget(self.add_eat_btn)
        row3.addItem(spacer)
        row3.addWidget(self.price_label)

        self.des_label.setAlignment(Qt.AlignLeft)

        row4 = QVBoxLayout()
        row4.setAlignment(Qt.AlignLeft)
        row4.addWidget(self.des_title)
        row4.addWidget(self.des_label)

        self.top_layout.addLayout(row0)
        self.top_layout.addLayout(row1)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.img_label, alignment=Qt.AlignCenter)
        self.top_layout.addStretch()
        self.top_layout.addLayout(row3)
        self.top_layout.addLayout(row4)
        self.top_layout.addStretch()
        
        self.setLayout(self.top_layout)

        # 子窗口
        self.add_eat.datepicker.setFixedWidth(200)
        self.add_eat.timepicker.setFixedWidth(200)
        self.add_eat.gridLayout = QGridLayout(self.add_eat)
        self.add_eat.gridLayout.setSpacing(10)
        self.add_eat.gridLayout.setContentsMargins(0, 150, 0, 0)
        self.add_eat.gridLayout.addWidget(self.add_eat.datepicker, 1, 0)
        self.add_eat.gridLayout.addWidget(self.add_eat.timepicker, 1, 1)
        self.add_eat.resize(500, 400)

        self.add_eat.save_btn.setEnabled(False)
        self.add_eat.gridLayout.addWidget(self.add_eat.save_btn, 2, 0, 1, 2, alignment=Qt.AlignCenter)
        self.add_eat.save_btn.setFixedSize(80, 40)
        self.add_eat.save_btn.setCursor(Qt.PointingHandCursor)

    def init_detail_func(self):
        # noinspection PyUnresolvedReferences
        self.star_btn.clicked.connect(lambda: self.star_dish())
        self.add_eat.datepicker.dateChanged.connect(self.set_date_able)
        self.add_eat.timepicker.timeChanged.connect(self.set_time_able)
        self.add_eat.save_btn.clicked.connect(self.set_date)

    def star_dish(self):
        if self.states.is_loggedin:
            user_model = (
                UserModel()
                .set_states(states=self.states)
                .fetch(uuid=self.states.user_uuid)
            )
            if self.star_btn.isChecked():
                create_success_info_bar(content="收藏成功", parent=self)
                user_model.add_favorite(dish_uuid=self.dish_model.uuid)
            else:
                create_success_info_bar(content="取消收藏成功", parent=self)
                user_model.remove_favorite(dish_uuid=self.dish_model.uuid)
        else:
            create_info_bar(title="提示", content="请先登录", parent=self)

    def show_picker(self):
        if self.states.is_loggedin:
            self.add_eat.show()
        else:
            create_info_bar(title="提示", content="请先登录", parent=self)

    def set_date(self):
        self.date = self.add_eat.datepicker.getDate()
        self.time = self.add_eat.timepicker.getTime()
        self.add_eat.close()
        # 改变icon
        self.add_eat_btn.setIcon(load_icon("eaten"))

        # 保存
        time_str = normalize(self.add_eat.datepicker.getDate(), self.add_eat.timepicker.getTime())
        create_success_info_bar(content=f"成功添加历史记录：{self.dish_model.name} {time_str}", parent=self)
        # 调用delete
        # 调用个人用户的添加记录
        user_model = (
            UserModel()
            .set_states(states=self.states)
            .fetch(uuid=self.states.user_uuid)
        )
        user_model.add_record(dish_uuid=self.dish_model.uuid, time=time_str)

    def get_date(self):
        return self.date

    def set_date_able(self):
        self.date_flag = True
        if self.time_flag:
            self.add_eat.save_btn.setEnabled(True)

    def set_time_able(self):
        self.time_flag = True
        if self.date_flag:
            self.add_eat.save_btn.setEnabled(True)

    def update_info(self):
        self.name_label.setText(self.dish_model.name)
        self.tags_label = QLabel("|".join(self.dish_model.tags))

        # 对star-btn和add eat btn进行刷新
        if self.states.is_loggedin:
            user_model = (
                UserModel()
                .set_states(states=self.states)
                .fetch(uuid=self.states.user_uuid)
            )
            self.add_eat_btn.setIcon(load_icon("eaten")
                                    if user_model.check_record(dish_uuid=self.dish_model.uuid) 
                                    else load_icon("addeat"))

        # 所有的组件
        self.counters.clear()
        for counter_uuid in self.dish_model.counters_uuids:
            counter_model = (
                CounterModel()
                .set_states(states=self.states)
                .fetch(uuid=counter_uuid)
            )
            canteen_model = (
                CanteenModel()
                .set_states(states=self.states)
                .fetch(uuid=counter_model.canteen_uuid)
            )
            self.counters.append(f"{canteen_model.name}{counter_model.name}")
        self.counter_label.setText("|".join(self.counters))

        self.rating_label.setText(str(self.dish_model.rating_average))

        image_model = (
            ImageModel()
            .set_states(states=self.states)
            .fetch(uuid=self.dish_model.image_uuid)
        )
        self.img_label = ImageLabel(crop_scale(image_model.to_image(), 80, 80))
        self.price_label.setText(f"￥{self.dish_model.price}")
        self.des_label.setText(self.dish_model.description)
