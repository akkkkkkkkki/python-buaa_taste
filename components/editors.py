from typing import Dict, List, Optional

from PySide6.QtGui import (QImage)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from backend import DishNotFound, UnauthorizedAccess
from components.comboboxes import CanteenCounterComboBoxes
from components.dialogs import open_image_file
from components.infobars import (create_error_info_bar, create_success_info_bar, create_warning_info_bar)
from components.mypage import MyPage
from models import CanteenModel
from models.counter import CounterModel
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.image import ImageModel
from qmaterialwidgets import (
    BodyLabel, ComboBox, DoubleSpinBox, ElevatedPushButton,
    FluentIcon,
    LineEdit,
    TextEdit
)


class AddOrEditDish(QWidget):
    def __init__(
            self, *,
            dish_model: Optional[DishModel],
            states: FrontendStates,
            page: MyPage,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self.dish_model: Optional[DishModel] = dish_model
        self.states: FrontendStates = states
        self.image: Optional[ImageModel] = None
        self.page: MyPage = page
        self.selected_counters: set[Optional[CounterModel]] = {
            CounterModel()
            .set_states(states=states)
            .fetch(uuid=counter_uuid)
            for counter_uuid in dish_model.counters_uuids
        } if dish_model is not None else set()
        self.combo_boxes_pairs: List[CanteenCounterComboBoxes] = []

        self.layout = QVBoxLayout()
        self.edit_name_label = BodyLabel('菜品名称', None)
        self.name_line_edit = LineEdit()
        self.edit_counter_title_layout = QHBoxLayout()
        self.edit_counter_label = BodyLabel('食堂及柜台', None)
        self.add_counter_button = ElevatedPushButton('添加', None, FluentIcon.ADD)
        self.combo_boxes_layout = QVBoxLayout()
        self.price_layout = QHBoxLayout()
        self.price_edit_label = BodyLabel('菜品价格', None)
        self.price_spin_box = DoubleSpinBox()
        self.edit_description_label = BodyLabel('菜品描述', None)
        self.description_text_edit = TextEdit()
        self.tags_label = BodyLabel('菜品标签', None)
        self.tags_edit = LineEdit()
        self.edit_image_title_layout = QHBoxLayout()
        self.edit_image_label = BodyLabel('菜品图片', None)
        self.delete_image_button = ElevatedPushButton('删除', None, FluentIcon.DELETE)
        self.image_button = ElevatedPushButton('上传', None, FluentIcon.PHOTO)
        self.image_label = QLabel()

        self.init_dish_add_edit_ui()
        self.init_dish_add_edit_func()

    def init_dish_add_edit_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.edit_name_label)
        self.layout.addWidget(self.name_line_edit)
        self.layout.addLayout(self.edit_counter_title_layout)
        self.edit_counter_title_layout.addWidget(self.edit_counter_label)
        self.edit_counter_title_layout.addStretch()
        self.edit_counter_title_layout.addWidget(self.add_counter_button)
        self.layout.addLayout(self.combo_boxes_layout)
        self.layout.addLayout(self.price_layout)
        self.price_layout.addWidget(self.price_edit_label)
        self.price_layout.addStretch()
        self.price_layout.addWidget(self.price_spin_box)
        self.layout.addWidget(self.tags_label)
        self.layout.addWidget(self.tags_edit)
        self.layout.addWidget(self.edit_description_label)
        self.layout.addWidget(self.description_text_edit)
        self.layout.addLayout(self.edit_image_title_layout)
        self.edit_image_title_layout.addWidget(self.edit_image_label)
        self.edit_image_title_layout.addStretch()
        self.edit_image_title_layout.addWidget(self.delete_image_button)
        self.edit_image_title_layout.addWidget(self.image_button)
        self.layout.addWidget(self.image_label)

        self.edit_name_label.setContentsMargins(0, 16, 0, 0)
        self.edit_counter_title_layout.setContentsMargins(0, 16, 0, 0)
        self.tags_label.setContentsMargins(0, 16, 0, 0)
        self.price_layout.setContentsMargins(0, 16, 0, 0)
        self.edit_description_label.setContentsMargins(0, 16, 0, 0)
        self.edit_image_title_layout.setContentsMargins(0, 16, 0, 0)

        self.setMinimumWidth(600)

        self.price_spin_box.setDecimals(2)
        self.price_spin_box.setMinimum(0.00)
        self.price_spin_box.setMaximum(100.00)
        self.price_spin_box.setValue(0.00)

        self.delete_image_button.setHidden(True)

    # noinspection PyUnresolvedReferences
    def init_dish_add_edit_func(self):
        if self.dish_model is not None:
            self.name_line_edit.setText(self.dish_model.name)
            self.selected_counters = {
                CounterModel()
                .set_states(states=self.states)
                .fetch(uuid=counter_uuid)
                for counter_uuid in self.dish_model.counters_uuids
            }
            self.tags_edit.setText(" ".join(self.dish_model.tags))
            self.price_spin_box.setValue(self.dish_model.price)
            self.description_text_edit.setText(self.dish_model.description)
            self.image = (
                ImageModel()
                .set_states(states=self.states)
                .fetch(uuid=self.dish_model.image_uuid)
            )
            self.image_label.setPixmap(self.image.to_pixmap().scaledToWidth(600))
        for counter in self.selected_counters:
            self.create_combo_boxes_pair(init_counter=counter)
        self.add_counter_button.clicked.connect(
            self.create_combo_boxes_pair
        )
        self.image_button.clicked.connect(
            self.on_clicked_upload_image
        )
        self.delete_image_button.clicked.connect(
            self.on_clicked_delete_image
        )
        self.name_line_edit.textChanged.connect(self.limit_text_length)
        self.tags_edit.textChanged.connect(self.limit_text_length)
        self.description_text_edit.textChanged.connect(self.limit_text_length)

    def update_options(self):
        self.selected_counters.clear()
        for pair in self.combo_boxes_pairs:
            if pair.current_counter is not None:
                self.selected_counters.add(pair.current_counter)
                print(self.selected_counters)
        for pair in self.combo_boxes_pairs:
            pair.init_counter_options()

    def create_combo_boxes_pair(self, *, init_counter: Optional[CounterModel] = None):
        combo_box_pair = CanteenCounterComboBoxes(
            states=self.states,
            init_counter=init_counter,
            selected_counters=self.selected_counters,
            page=self.page
        )
        combo_box_pair.delete_button_func = self.delete_counter_func(combo_box_pair)
        combo_box_pair.update_all_func = self.update_options
        self.combo_boxes_pairs.append(combo_box_pair)
        self.combo_boxes_layout.addWidget(combo_box_pair)

    def delete_counter_func(self, widget: CanteenCounterComboBoxes):
        def make_func():
            self.combo_boxes_layout.removeWidget(widget)
            widget.deleteLater()
            self.update_options()

        return make_func

    def on_clicked_upload_image(self):
        image_data = open_image_file(parent=self.page)
        self.image = ImageModel().from_data(data=image_data)
        pixmap = self.image.to_pixmap().scaledToWidth(600)
        if pixmap.isNull():
            create_error_info_bar('未能加载图片，请尝试其他图片及格式。', parent=self.page.get_root())
        else:
            self.image_label.setPixmap(pixmap)
            self.image_button.setHidden(True)
            self.delete_image_button.setHidden(False)

    def on_clicked_delete_image(self):
        self.image = QImage()
        self.image_label.clear()
        self.delete_image_button.setHidden(True)
        self.image_button.setHidden(False)

    def limit_text_length(self):
        if len(self.name_line_edit.text()) > 10:
            create_warning_info_bar('菜品名不超过 10 个字。', self.page.get_root())
            self.name_line_edit.setText(self.name_line_edit.text()[:10])
        if len(self.tags_edit.text()) > 16:
            self.tags_edit.setText(self.tags_edit.text()[:16])
            create_warning_info_bar('标签包含空白总共不超过 16 个字。', self.page.get_root())
        if len(self.description_text_edit.toPlainText()) > 100:
            self.description_text_edit.setText(self.description_text_edit.toPlainText()[:100])
            create_warning_info_bar('描述不超过 100 个字。', self.page.get_root())

    @property
    def available(self) -> bool:
        available = True
        all_dishes = DishModel.get_all_dishes(states=self.states)
        if self.dish_model is None:
            for dish in all_dishes:
                if dish.name == self.name_line_edit.text():
                    available = False
                    create_error_info_bar('菜品名和现有重复。', self.page.get_root())
        if len(self.name_line_edit.text()) == 0:
            available = False
            create_error_info_bar('菜品名不能为空', self.page.get_root())
        if len(self.tags_edit.text()) == 0:
            available = False
            create_error_info_bar('至少添加一个标签', self.page.get_root())
        if len(self.description_text_edit.toPlainText()) == 0:
            available = False
            create_error_info_bar('菜品描述不能为空', self.page.get_root())
        if len(self.selected_counters) == 0:
            available = False
            create_error_info_bar('至少添加一个柜台', self.page.get_root())
        if self.image is None:
            available = False
            create_error_info_bar('必须添加一张图片', self.page.get_root())
        return available

    def save_content(self):
        available = self.available
        if self.dish_model is not None and available:
            try:
                self.page.show_spiner()
                self.dish_model.modify(
                    name=self.name_line_edit.text(),
                    tags=self.tags_edit.text().split(' '),
                    description=self.description_text_edit.toPlainText(),
                    price=self.price_spin_box.value(),
                    image=self.image if self.image is not None else None,
                    counters_uuids=[
                        counter.uuid
                        for counter in self.selected_counters
                    ]
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功保存内容。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
        elif available:
            try:
                self.page.show_spiner()
                DishModel.add(
                    states=self.states,
                    name=self.name_line_edit.text(),
                    tags=self.tags_edit.text().split(' '),
                    description=self.description_text_edit.toPlainText(),
                    price=self.price_spin_box.value(),
                    image=self.image if self.image is not None else None,
                    counters_uuids=[
                        counter.uuid
                        for counter in self.selected_counters
                    ]
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功添加菜品。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
            except DishNotFound as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())


class AddOrEditCanteen(QWidget):
    def __init__(
            self, *,
            canteen_model: Optional[CanteenModel],
            states: FrontendStates,
            page: MyPage,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self.canteen_model: Optional[CanteenModel] = canteen_model
        self.states: FrontendStates = states
        self.image: Optional[ImageModel] = None
        self.page: MyPage = page

        self.layout = QVBoxLayout()
        self.edit_name_label = BodyLabel('食堂名称', None)
        self.name_line_edit = LineEdit()
        self.edit_description_label = BodyLabel('食堂描述', None)
        self.description_text_edit = TextEdit()
        self.edit_image_title_layout = QHBoxLayout()
        self.edit_image_label = BodyLabel('食堂图片', None)
        self.delete_image_button = ElevatedPushButton('删除', None, FluentIcon.DELETE)
        self.image_button = ElevatedPushButton('上传', None, FluentIcon.PHOTO)
        self.image_label = QLabel()

        self.init_dish_add_edit_ui()
        self.init_canteen_add_edit_func()

    def init_dish_add_edit_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.edit_name_label)
        self.layout.addWidget(self.name_line_edit)
        self.layout.addWidget(self.edit_description_label)
        self.layout.addWidget(self.description_text_edit)
        self.layout.addLayout(self.edit_image_title_layout)
        self.edit_image_title_layout.addWidget(self.edit_image_label)
        self.edit_image_title_layout.addStretch()
        self.edit_image_title_layout.addWidget(self.delete_image_button)
        self.edit_image_title_layout.addWidget(self.image_button)
        self.layout.addWidget(self.image_label)

        self.edit_name_label.setContentsMargins(0, 16, 0, 0)
        self.edit_description_label.setContentsMargins(0, 16, 0, 0)
        self.edit_image_title_layout.setContentsMargins(0, 16, 0, 0)

        self.setMinimumWidth(600)
        self.delete_image_button.setHidden(True)

    # noinspection PyUnresolvedReferences
    def init_canteen_add_edit_func(self):
        if self.canteen_model is not None:
            self.name_line_edit.setText(self.canteen_model.name)
            self.description_text_edit.setText(self.canteen_model.description)
            self.image = (
                ImageModel()
                .set_states(states=self.states)
                .fetch(uuid=self.canteen_model.image_uuid)
            )
            self.image_label.setPixmap(self.image.to_pixmap().scaledToWidth(600))
        self.image_button.clicked.connect(
            self.on_clicked_upload_image
        )
        self.delete_image_button.clicked.connect(
            self.on_clicked_delete_image
        )
        self.name_line_edit.textChanged.connect(self.limit_text_length)
        self.description_text_edit.textChanged.connect(self.limit_text_length)

    def on_clicked_upload_image(self):
        image_data = open_image_file(parent=self.page)
        self.image = ImageModel().from_data(data=image_data)
        pixmap = self.image.to_pixmap().scaledToWidth(600)
        if pixmap.isNull():
            create_error_info_bar('未能加载图片，请尝试其他图片及格式。', parent=self.page.get_root())
        else:
            self.image_label.setPixmap(pixmap)
            self.image_button.setHidden(True)
            self.delete_image_button.setHidden(False)

    def on_clicked_delete_image(self):
        self.image = QImage()
        self.image_label.clear()
        self.delete_image_button.setHidden(True)
        self.image_button.setHidden(False)

    def limit_text_length(self):
        if len(self.name_line_edit.text()) > 10:
            create_warning_info_bar('食堂名不超过 10 个字。', self.page.get_root())
            self.name_line_edit.setText(self.name_line_edit.text()[:10])
        if len(self.description_text_edit.toPlainText()) > 100:
            self.description_text_edit.setText(self.description_text_edit.toPlainText()[:100])
            create_warning_info_bar('描述不超过 100 个字。', self.page.get_root())

    @property
    def available(self) -> bool:
        available = True
        all_canteens = CanteenModel.get_all(states=self.states)
        if self.canteen_model is None:
            for canteen in all_canteens:
                if canteen.name == self.name_line_edit.text():
                    available = False
                    create_error_info_bar('食堂名和现有重复。', self.page.get_root())
        if len(self.name_line_edit.text()) == 0:
            available = False
            create_error_info_bar('食堂名不能为空', self.page.get_root())
        if len(self.description_text_edit.toPlainText()) == 0:
            available = False
            create_error_info_bar('菜品描述不能为空', self.page.get_root())
        if self.image is None:
            available = False
            create_error_info_bar('必须添加一张图片', self.page.get_root())
        return available

    def save_content(self):
        available = self.available
        if self.canteen_model is not None and available:
            try:
                self.page.show_spiner()
                self.canteen_model.modify(
                    name=self.name_line_edit.text(),
                    description=self.description_text_edit.toPlainText(),
                    image=self.image if self.image is not None else None,
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功保存内容。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
        elif available:
            try:
                self.page.show_spiner()
                CanteenModel.add(
                    states=self.states,
                    name=self.name_line_edit.text(),
                    description=self.description_text_edit.toPlainText(),
                    image=self.image if self.image is not None else None,
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功添加食堂。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
            except DishNotFound as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())


class AddOrEditCounter(QWidget):
    def __init__(
            self, *,
            counter_model: Optional[CounterModel],
            states: FrontendStates,
            page: MyPage,
            parent: QWidget = None
    ):
        super().__init__(parent)
        self.canteen_name_to_model: Dict[str, CanteenModel] = {}
        self.counter_model: Optional[CounterModel] = counter_model
        self.states: FrontendStates = states
        self.image: Optional[ImageModel] = None
        self.page: MyPage = page
        self.selected_canteen: Optional[CounterModel] = (
            CounterModel()
            .set_states(states=states)
            .fetch(uuid=counter_model.canteen_uuid)
        ) if counter_model is not None else None

        self.layout = QVBoxLayout()
        self.edit_name_label = BodyLabel('柜台名称', None)
        self.name_line_edit = LineEdit()
        self.edit_canteen_label = BodyLabel('选择食堂', None)
        self.edit_canteen_box = ComboBox()
        self.edit_description_label = BodyLabel('柜台描述', None)
        self.description_text_edit = TextEdit()
        self.edit_image_title_layout = QHBoxLayout()
        self.edit_image_label = BodyLabel('柜台图片', None)
        self.delete_image_button = ElevatedPushButton('删除', None, FluentIcon.DELETE)
        self.image_button = ElevatedPushButton('上传', None, FluentIcon.PHOTO)
        self.image_label = QLabel()

        self.init_counter_add_edit_ui()
        self.init_counter_add_edit_func()

    def init_counter_add_edit_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.edit_name_label)
        self.layout.addWidget(self.name_line_edit)
        self.layout.addWidget(self.edit_canteen_label)
        self.layout.addWidget(self.edit_canteen_box)
        self.layout.addWidget(self.edit_description_label)
        self.layout.addWidget(self.description_text_edit)
        self.layout.addLayout(self.edit_image_title_layout)
        self.edit_image_title_layout.addWidget(self.edit_image_label)
        self.edit_image_title_layout.addStretch()
        self.edit_image_title_layout.addWidget(self.delete_image_button)
        self.edit_image_title_layout.addWidget(self.image_button)
        self.layout.addWidget(self.image_label)

        self.edit_name_label.setContentsMargins(0, 16, 0, 0)
        self.edit_canteen_label.setContentsMargins(0, 16, 0, 0)
        self.edit_description_label.setContentsMargins(0, 16, 0, 0)
        self.edit_image_title_layout.setContentsMargins(0, 16, 0, 0)

        self.edit_canteen_box.setFixedWidth(600)
        self.setMinimumWidth(600)

        self.delete_image_button.setHidden(True)

    # noinspection PyUnresolvedReferences
    def init_counter_add_edit_func(self):
        if self.counter_model is not None:
            self.name_line_edit.setText(self.counter_model.name)
            self.selected_canteen = (
                CanteenModel()
                .set_states(states=self.states)
                .fetch(uuid=self.counter_model.canteen_uuid)
            )
            self.description_text_edit.setText(self.counter_model.description)
            self.image = (
                ImageModel()
                .set_states(states=self.states)
                .fetch(uuid=self.counter_model.image_uuid)
            )
            self.image_label.setPixmap(self.image.to_pixmap().scaledToWidth(600))
        self.canteen_name_to_model = {
            canteen_model.name: canteen_model
            for canteen_model in CanteenModel.get_all(states=self.states)
        }
        self.edit_canteen_box.addItems(self.canteen_name_to_model.keys())
        if self.selected_canteen is not None:
            self.edit_canteen_box.setText(self.selected_canteen.name)
        self.image_button.clicked.connect(self.on_clicked_upload_image)
        self.delete_image_button.clicked.connect(self.on_clicked_delete_image)
        self.name_line_edit.textChanged.connect(self.limit_text_length)
        self.description_text_edit.textChanged.connect(self.limit_text_length)

    def on_clicked_upload_image(self):
        image_data = open_image_file(parent=self.page)
        self.image = ImageModel().from_data(data=image_data)
        pixmap = self.image.to_pixmap().scaledToWidth(600)
        if pixmap.isNull():
            create_error_info_bar('未能加载图片，请尝试其他图片及格式。', parent=self.page.get_root())
        else:
            self.image_label.setPixmap(pixmap)
            self.image_button.setHidden(True)
            self.delete_image_button.setHidden(False)

    def on_clicked_delete_image(self):
        self.image = QImage()
        self.image_label.clear()
        self.delete_image_button.setHidden(True)
        self.image_button.setHidden(False)

    def limit_text_length(self):
        if len(self.name_line_edit.text()) > 10:
            create_warning_info_bar('柜台名不超过 10 个字。', self.page.get_root())
            self.name_line_edit.setText(self.name_line_edit.text()[:10])
        if len(self.description_text_edit.toPlainText()) > 100:
            self.description_text_edit.setText(self.description_text_edit.toPlainText()[:100])
            create_warning_info_bar('描述不超过 100 个字。', self.page.get_root())

    @property
    def available(self) -> bool:
        available = True
        all_dishes = DishModel.get_all_dishes(states=self.states)
        if self.counter_model is None:
            for dish in all_dishes:
                if dish.name == self.name_line_edit.text():
                    available = False
                    create_error_info_bar('柜台名和现有重复。', self.page.get_root())
        if len(self.name_line_edit.text()) == 0:
            available = False
            create_error_info_bar('柜台名不能为空', self.page.get_root())
        if len(self.description_text_edit.toPlainText()) == 0:
            available = False
            create_error_info_bar('柜台描述不能为空', self.page.get_root())
        if self.edit_canteen_box.currentIndex() == -1:
            available = False
            create_error_info_bar('至少选择一个食堂', self.page.get_root())
        if self.image is None:
            available = False
            create_error_info_bar('必须添加一张图片', self.page.get_root())
        return available

    def save_content(self):
        available = self.available
        if self.counter_model is not None and available:
            try:
                self.page.show_spiner()
                self.counter_model.modify(
                    name=self.name_line_edit.text(),
                    description=self.description_text_edit.toPlainText(),
                    image=self.image if self.image is not None else None,
                    canteen=self.canteen_name_to_model[self.edit_canteen_box.currentText()]
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功保存内容。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
        elif available:
            try:
                self.page.show_spiner()
                CounterModel.add(
                    states=self.states,
                    name=self.name_line_edit.text(),
                    description=self.description_text_edit.toPlainText(),
                    image=self.image if self.image is not None else None,
                    canteen=self.canteen_name_to_model[self.edit_canteen_box.currentText()]
                )
                self.page.hide_spiner()
                self.page.pop_page()
                create_success_info_bar('成功添加柜台。', parent=self.page.get_root())
            except UnauthorizedAccess as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
            except DishNotFound as e:
                create_error_info_bar(f'{e}', parent=self.page.get_root())
