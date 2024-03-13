from PySide6.QtWidgets import QApplication

from models.frontendstates import FrontendStates
from pages.login_page import LoginPage

if __name__ == '__main__':
    app = QApplication([])
    states = FrontendStates()
    window = LoginPage(states=states, parent=None)
    window.show()
    window.resize(1024, 768)
    app.exec()
