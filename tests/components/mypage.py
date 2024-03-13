import random

from PySide6.QtWidgets import QApplication

from models.frontendstates import FrontendStates
from components.mypage import MyPage
from qmaterialwidgets import FilledPushButton, TitleLabel


# noinspection PyUnresolvedReferences
def create_secondary_page(parent: MyPage) -> MyPage:
    secondary_page = MyPage(
        object_name='test1',
        page_name='adsd',
        states=FrontendStates(),
        prev_page=parent,
        backend=None
    )
    secondary_page.add_stretch()
    secondary_page.add_widget(TitleLabel(f'次级页面{random.randint(123, 456)}', None))
    secondary_page.add_stretch()

    open_secondary_window_button = FilledPushButton('打开次级页面', None)
    open_secondary_window_button.clicked.connect(
        lambda: parent.push_page(create_secondary_page(secondary_page))
    )

    secondary_page.add_widget(open_secondary_window_button)
    return secondary_page


if __name__ == '__main__':
    app = QApplication([])

    main_page = MyPage(
        object_name='test1',
        page_name='首页',
        states=FrontendStates(),
        prev_page=None,
        backend=None
    )
    main_page.add_stretch()
    main_page.add_widget(TitleLabel('首页'))
    main_page.add_stretch()

    open_secondary_window_button = FilledPushButton('打开次级页面')
    open_secondary_window_button.clicked.connect(
        lambda: main_page.push_page(create_secondary_page(main_page))
    )
    main_page.add_widget(open_secondary_window_button)

    main_page.show()
    main_page.resize(1024,768)

    app.exec()
