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


class DishInfoWidget(MyCard):
    def __init__(
            self, *,
            dish_model: DishModel,
            states: FrontendStates,
            page: MyPage,
            parent=None
    ):
        super(DishInfoWidget, self).__init__(
            360,
            100,
            Qt.Orientation.Horizontal,
            parent
        )
        self.states = states
        self.dish_model = dish_model
        self.page = page
        self.image = (
            ImageModel()
            .set_states(states=states)
            .fetch(uuid=dish_model.image_uuid)
        )
        self.middle_layout = QVBoxLayout()
        self.img_label = ImageLabel(
            crop_scale(
                pixmap=self.image.to_pixmap(),
                width=80,
                height=80
            )
        )
        self.name_label = BodyLabel(dish_model.name)
        self.tags_label = SecondaryLabel(
            truncate_text(
                text="｜".join(dish_model.tags),
                max_length=15
            )
        )
        self.rating_label = StarRating(
            rating=dish_model.rating_average,
            show_divider=False
        )
        self.price_label = SubtitleLabel(
            f"￥{dish_model.price}",
            None
        )

        self.init_dish_info_ui()
        self.init_functionality()

    def init_dish_info_ui(self) -> None:
        self.add_widget(self.img_label)
        self.add_layout(self.middle_layout)
        self.middle_layout.addWidget(self.name_label)
        self.middle_layout.addWidget(self.tags_label)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.rating_label)
        self.add_stretch()
        self.add_widget(self.price_label)
        self.setLayout(self.layout)

        self.set_padding(10, 10, 20, 10)
        self.middle_layout.setContentsMargins(10, 5, 10, 5)
        self.img_label.setContentsMargins(0, 0, 10, 0)
        self.name_label.setContentsMargins(4, 0, 0, 4)
        self.tags_label.setContentsMargins(4, 0, 0, 4)
        self.rating_label.setContentsMargins(0, 0, 0, 0)

        self.set_spacing(0)
        self.middle_layout.setSpacing(0)

        self.img_label.setFixedSize(80, 80)

    def init_functionality(self) -> None:
        self.setObjectName('dish-item-' + self.name_label.text())

    def update_info(self):
        self.image = (
            ImageModel()
            .set_states(states=self.states)
            .fetch(uuid=self.dish_model.image_uuid)
        )
        self.img_label = ImageLabel(
            crop_scale(
                pixmap=self.image.to_pixmap(),
                width=80,
                height=80
            )
        )
        self.name_label.setText(self.dish_model.name)
        self.tags_label.setText(truncate_text(
                text="｜".join(self.dish_model.tags),
                max_length=15
            ))
        self.rating_label.set_rating(rating=self.dish_model.rating_average)
        self.price_label.setText(f"￥{self.dish_model.price}")