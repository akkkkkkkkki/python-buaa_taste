from PySide6.QtWidgets import QApplication

from models.frontendstates import FrontendStates
from pages.search_page import SearchPage


def test() -> None:
    app = QApplication([])

    window = SearchPage(states=FrontendStates())
    window.resize(1024, 768)
    window.show()

    app.exec()

if __name__ == '__main__':
    test()
