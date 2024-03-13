from PySide6.QtWidgets import QApplication

from generator import generate_simple_tile_item
from tests.components.TestWindow import MyTestWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MyTestWindow(500, 500)

    tile, _ = generate_simple_tile_item()
    window.add_widget(tile)

    app.exec()
