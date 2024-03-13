from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout

from models.frontendstates import FrontendStates
from models.user import UserModel
from my_helpers import load_icon
from pages.classification_page import ClassificationPage
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.user_page import UserPage
from qmaterialwidgets import FluentIcon, MaterialWindow
from qmaterialwidgets import NavigationItemPosition, setFont, SubtitleLabel, SplashScreen


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Main(MaterialWindow):
    """
    主页面。
    """

    def __init__(self):
        super(Main, self).__init__()
        self.states = FrontendStates()
        self.user_model = UserModel().set_states(states=self.states)

        # 设置窗口属性。
        self.init_window()

        # 创建子页面。
        self.home_page = HomePage(
            states=self.states,
            user_model=self.user_model
        )
        self.home_page.rerender.emit()
        self.search_page = SearchPage(self.states, None)
        self.category_page = ClassificationPage(
            states=self.states,
            user_model=self.user_model,
            prev_page=None
        )
        self.category_page.rerender.emit()
        self.user_page = UserPage(
            states=self.states,
            user_model=self.user_model
        )

        self.states.set_pages(
            home_page=self.home_page,
            search_page=self.search_page,
            category_page=self.category_page,
            user_page=self.user_page
        )

        # 设置侧边导航栏。
        self.init_navigation()        

        self.splash_screen.finish()

    # 设置侧边导航栏
    def init_navigation(self):
        home_button = self.addSubInterface(
            interface=self.home_page,
            icon=FluentIcon.HOME,
            text='主页',
            selectedIcon=FluentIcon.HOME_FILL,
            position=NavigationItemPosition.TOP
        )

        search_button = self.addSubInterface(
            interface=self.search_page,
            icon=FluentIcon.SEARCH,
            text='搜索',
            position=NavigationItemPosition.TOP
        )

        category_button = self.addSubInterface(
            interface=self.category_page,
            icon=FluentIcon.BOOK_SHELF,
            text='分类',
            position=NavigationItemPosition.TOP
        )

        user_button = self.addSubInterface(
            interface=self.user_page,
            icon=FluentIcon.PEOPLE,
            text='用户中心',
            position=NavigationItemPosition.BOTTOM
        )

        home_button.clicked.connect(self.home_page.update_info)
        search_button.clicked.connect(self.search_page.update_info)
        category_button.clicked.connect(self.category_page.update_info)
        user_button.clicked.connect(self.user_page.update_info)

        # 基于 objectName 设置默认页面
        self.navigationInterface.setCurrentItem(self.home_page.objectName())

    # 初始化窗口属性
    def init_window(self):
        self.resize(1024, 768)
        self.setMinimumSize(1024, 768)
        self.setWindowIcon(load_icon('logo')) # 为了splash window提前了
        self.setWindowTitle('航味 - 航的味道我知道')

        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(120, 120))
        self.splash_screen.raise_()

        # 设置窗口居中显示
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    main_window = Main()
    main_window.show()
    app.exec()
