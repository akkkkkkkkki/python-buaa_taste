from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from components.mypage import MyPage
from components.myuser import Login

if __name__ == '__main__':
    app = QApplication([])
    window = MyPage(
        'login-page',
        '登录页',
        None,
        None,
        None
    )
    widget = Login()
    window.add_stretch()
    window.add_widget(widget, alignment=Qt.AlignmentFlag.AlignHCenter)
    window.add_spacing(32)
    window.add_stretch()
    window.show()
    window.resize(1024, 768)
    app.exec()
