from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget

from components.mylabel import SecondaryLabel
from qmaterialwidgets import BodyLabel, FluentIcon, TransparentToolButton


class TextItem(QWidget):
    def __init__(
            self, *,
            main_text: str,
            secondary_text: str,
            parent: QWidget = None
    ):
        super(TextItem, self).__init__(parent)

        self.main_label = BodyLabel(main_text, self)
        self.secondary_label = SecondaryLabel(secondary_text)
        self.layout = QVBoxLayout()

        self.init_text_item_ui()

    def init_text_item_ui(self):
        self.setLayout(self.layout)
        self.layout.addStretch()
        self.layout.addWidget(
            self.main_label,
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.layout.addWidget(
            self.secondary_label,
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.layout.addStretch()

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(4)

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

    def set_text(self, *, main_text: str, secondary_text: str):
        self.main_label.setText(main_text)
        self.main_label.setText(secondary_text)
        return self

    def disable_secondary_text(self):
        self.secondary_label.setHidden(True)


class ListItem(QWidget):
    def __init__(self, *, widget: QWidget, parent: QWidget = None):
        super(ListItem, self).__init__(parent)
        self.parent_list = None
        self.widget = widget

        self.item_widget = None
        self.delete_button = TransparentToolButton(FluentIcon.DELETE, None)

        self.layout = QHBoxLayout()

        self.init_list_item_ui()

    def init_list_item_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.widget)
        self.layout.addStretch()
        self.layout.addWidget(self.delete_button)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
