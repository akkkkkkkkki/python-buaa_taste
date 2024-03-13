from typing import Any, Callable

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QVBoxLayout

from components.mycard import MyCard
from components.mylabel import (
    BoldBodyLabel,
    SecondaryLabel
)
from components.mypage import MyPage
from components.star_rating import StarRating
from models import CanteenModel, CounterModel
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.user import UserModel
from models.image import ImageModel
from my_helpers import (
    crop_scale,
    truncate_text
)
from pages.detail_page import DetailPage
from qmaterialwidgets import (
    BodyLabel, ImageLabel,
    SubtitleLabel
)


class CanteenCounterInfo(MyCard):
    def __init__(
            self, *,
            model: CanteenModel | CounterModel,
            states: FrontendStates,
            page: MyPage,
            parent=None
    ):
        super(CanteenCounterInfo, self).__init__(
            360,
            100,
            Qt.Orientation.Horizontal,
            parent
        )
        self.states = states
        self.model = model
        self.page = page
        self.image = (
            ImageModel()
            .set_states(states=states)
            .fetch(uuid=model.image_uuid)
        )
        self.middle_layout = QVBoxLayout()
        self.img_label = ImageLabel(
            crop_scale(
                pixmap=self.image.to_pixmap(),
                width=80,
                height=80
            )
        )
        self.name_label = BodyLabel(model.name)
        self.description_label = SecondaryLabel(
            truncate_text(
                text=model.description,
                max_length=15
            )
        )

        self.init_dish_info_ui()
        self.init_functionality()

    def init_dish_info_ui(self) -> None:
        self.add_widget(self.img_label)
        self.add_layout(self.middle_layout)
        self.middle_layout.addWidget(self.name_label)
        self.middle_layout.addWidget(self.description_label)
        self.middle_layout.addStretch()
        self.add_stretch()
        self.setLayout(self.layout)

        self.set_padding(10, 10, 20, 10)
        self.middle_layout.setContentsMargins(10, 5, 10, 5)
        self.img_label.setContentsMargins(0, 0, 10, 0)
        self.name_label.setContentsMargins(4, 0, 0, 4)
        self.description_label.setContentsMargins(4, 0, 0, 4)

        self.set_spacing(0)
        self.middle_layout.setSpacing(0)

        self.img_label.setFixedSize(80, 80)

    def init_functionality(self) -> None:
        self.setObjectName('canteen-or-counter-item-' + self.name_label.text())

    def update_info(self):
        self.image = (
            ImageModel()
            .set_states(states=self.states)
            .fetch(uuid=self.model.image_uuid)
        )
        self.img_label = ImageLabel(
            crop_scale(
                pixmap=self.image.to_pixmap(),
                width=80,
                height=80
            )
        )
        self.name_label.setText(self.model.name)
        self.description_label.setText(truncate_text(
                text=self.model.description,
                max_length=15
            ))
