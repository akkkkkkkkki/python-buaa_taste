from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget


class MyTestWindow(QFrame):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show()
        self.resize(width, height)

    def add_widget(self, widget: QWidget) -> None:
        self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)
