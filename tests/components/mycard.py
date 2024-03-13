from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from components.mycard import MyCard
from components.mypage import MyPage
from models.frontendstates import FrontendStates
from qmaterialwidgets import TitleLabel


class TestCard(MyCard):
    def __init__(self, width: int, height: int, orientation: Qt.Orientation, parent: QWidget = None):

        super().__init__(width, height, orientation, parent)
        self.add_widget(
            TitleLabel('一张卡片'),
            alignment=Qt.AlignmentFlag.AlignCenter
        )

    def on_click(self) -> None:
        super(TestCard, self).on_click()
        print('点击了卡片')


if __name__ == '__main__':
    app = QApplication([])
    window = MyPage(
        'page',
        '卡片及动画及功能测试',
        FrontendStates(),
        None,
        None
    )
    window.add_stretch()
    card = TestCard(300, 200, parent=window)
    window.add_widget(card)
    window.add_stretch()
    window.show()
    window.resize(500, 500)
    app.exec()
