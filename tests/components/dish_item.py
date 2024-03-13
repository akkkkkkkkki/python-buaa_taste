from PySide6.QtWidgets import QApplication

from tests.components.TestWindow import MyTestWindow
from generator import generate_dish_item

if __name__ == "__main__":
    app = QApplication([])
    window = MyTestWindow(500, 500)
    widget, _ = generate_dish_item()
    window.add_widget(widget)
    app.exec()
