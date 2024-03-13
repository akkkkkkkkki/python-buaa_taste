from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from components.mycard import MyCard
from components.mylabel import BoldBodyLabel, SecondaryLabel
from models.frontendstates import FrontendStates
from my_helpers import bytes_to_pixmap, crop_scale, truncate_text
from qmaterialwidgets import FluentIcon, ImageLabel, MessageBox, TransparentToolButton


class SimpleTile(MyCard):

    def __init__(
            self,
            name: str,
            description: str,
            image: bytes,
            backend,
            states: FrontendStates,
            parent=None
    ):
        super().__init__(360, 100, Qt.Orientation.Horizontal, parent)
        self.states = states

        self.img_label = ImageLabel(crop_scale(bytes_to_pixmap(image), 80, 80))
        self.name_label = BoldBodyLabel(name)
        self.description_label = SecondaryLabel(truncate_text(description, 30))
        self.more_button = TransparentToolButton(FluentIcon.DELETE, self)

        self.middle_layout = QVBoxLayout()

        self.init_tile_ui()
        self.init_functionality()

    def init_tile_ui(self) -> None:
        self.add_widget(self.img_label)
        self.add_layout(self.middle_layout)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.name_label)
        self.middle_layout.addWidget(self.description_label)
        self.middle_layout.addStretch()
        self.add_stretch()
        self.add_widget(self.more_button)

        self.set_padding(10, 10, 10, 10)
        self.middle_layout.setContentsMargins(10, 5, 10, 5)
        self.name_label.setContentsMargins(0, 0, 0, 4)
        self.description_label.setContentsMargins(0, 0, 0, 0)

        self.set_spacing(0)
        self.middle_layout.setSpacing(0)
        self.middle_layout.setContentsMargins(12, 0, 0, 0)

        self.img_label.setFixedSize(80, 80)

        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    def init_functionality(self):
        self.setObjectName('tile-' + self.name_label.text())
        self.more_button.clicked.connect(self.on_click_more_button)

    def on_click(self) -> None:
        super().on_click()
        print(f'点击了卡片{self.objectName()}')

    @Slot()
    def on_click_more_button(self) -> None:
        print(f"点击了卡片{self.objectName()}的按钮。")


# noinspection DuplicatedCode
class TextTile(MyCard):
    def __init__(
            self,
            name: str,
            description: str,
            space: QWidget,
            parent=None
    ):
        super().__init__(360, 100, Qt.Orientation.Horizontal, parent)
        self.space = space

        self.name_label = BoldBodyLabel(name)
        self.description_label = SecondaryLabel(truncate_text(description, 30))
        self.more_button = TransparentToolButton(FluentIcon.DELETE, self)
        self.on_click_func = None
        self.on_click_button_func = None

        self.middle_layout = QVBoxLayout()

        self.init_tile_ui()
        self.init_functionality()

    def init_tile_ui(self) -> None:
        self.add_layout(self.middle_layout)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.name_label)
        self.middle_layout.addWidget(self.description_label)
        self.middle_layout.addStretch()
        self.add_stretch()
        self.add_widget(self.more_button)

        self.set_padding(10, 10, 10, 10)
        self.middle_layout.setContentsMargins(0, 5, 10, 5)
        self.name_label.setContentsMargins(0, 0, 0, 4)
        self.description_label.setContentsMargins(0, 0, 0, 0)

        self.set_spacing(0)
        self.middle_layout.setSpacing(0)
        self.middle_layout.setContentsMargins(12, 0, 0, 0)

        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    # noinspection PyUnresolvedReferences
    def init_functionality(self):
        self.setObjectName('tile-' + self.name_label.text())
        self.more_button.clicked.connect(self.on_click_button)

    def on_click(self) -> None:
        super().on_click()
        self.on_click_func()
        print(f'点击了卡片{self.objectName()}')

    @Slot()
    def on_click_button(self) -> None:
        title = '你确定要删除吗?'
        content = """次操作不可恢复"""
        w = MessageBox(title, content, self.space)

        if w.exec():
            self.on_click_button_func()
