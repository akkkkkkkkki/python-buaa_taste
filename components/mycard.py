from typing import final, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLayout, QVBoxLayout, QWidget

from components.shadow import ShadowAnimation


class MyCard(ShadowAnimation, QFrame):
    def __init__(self,
                 width: int,
                 height: int,
                 orientation: Qt.Orientation,
                 parent: QWidget = None):
        super(MyCard, self).__init__(parent)
        self.width = width
        self.height = height

        if orientation == Qt.Orientation.Vertical:
            self.layout = QVBoxLayout()
        else:
            self.layout = QHBoxLayout()

        self.init_card_ui()
        self.setObjectName('myCard')

    @final
    def init_card_ui(self) -> None:
        self.setFixedSize(self.width, self.height)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: white; border-radius: 10px;")
        self.apply_effect(self)
        self.setLayout(self.layout)

    @final
    def add_widget(
            self,
            widget: QWidget,
            alignment: Optional[Qt.AlignmentFlag] = None
    ) -> None:
        if alignment is None:
            self.layout.addWidget(widget)
        else:
            self.layout.addWidget(widget, alignment=alignment)

    @final
    def add_layout(
            self,
            layout: QLayout,
            stretch: Optional[int] = None,
    ) -> None:
        if stretch is None:
            self.layout.addLayout(layout)
        else:
            self.layout.addLayout(layout, stretch=stretch)

    @final
    def add_spacing(
            self,
            spacing: int
    ) -> None:
        self.layout.addSpacing(spacing)

    @final
    def add_stretch(
            self,
            strectch: Optional[int] = None
    ):
        if strectch is None:
            self.layout.addStretch()
        else:
            self.layout.addStretch(stretch=strectch)

    @final
    def set_padding(self, left: int, top: int, right: int, bottom: int) -> None:
        self.layout.setContentsMargins(left, top, right, bottom)

    @final
    def set_spacing(self, spacing: int) -> None:
        self.layout.setSpacing(spacing)

    def clear(self) -> None:
        while self.layout.count() > 0:
            item = self.layout.itemAt(0)
            widget = item.widget()
            self.layout.removeItem(item)
            widget.deleteLater()
