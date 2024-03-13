from typing import final, List

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLayout,
    QVBoxLayout,
    QWidget
)

from models.frontendstates import FrontendStates
from qmaterialwidgets import (
    BodyLabel,
    IndeterminateProgressBar, ScrollArea, TextPushButton
)
from qmaterialwidgets import FluentIcon


class MyPage(QFrame):
    def __init__(self, *,
                 object_name: str,
                 page_name: str,
                 states: FrontendStates,
                 prev_page,
                 parent=None):
        super(MyPage, self).__init__(parent)
        self.parent = parent
        self.setObjectName(object_name)
        self.disable_further_return: bool = False

        self.page_name: str = page_name
        self.states: FrontendStates = states
        self.prev_page: MyPage = prev_page
        self._pages: List[MyPage] = []

        self._return_button = TextPushButton("返回", None, FluentIcon.RETURN)
        self._breadcrumb_text = BodyLabel(self.page_name, None)
        self._scroll_area = ScrollArea()
        self._container = QFrame()
        self._whole_page = QFrame()
        self._content = QFrame()
        self.in_progress_bar = IndeterminateProgressBar()

        self._scroll_layout = QVBoxLayout()
        self._page_layout = QVBoxLayout()
        self._nav_layout = QHBoxLayout()
        self._content_layout = QVBoxLayout()

        self.init_my_page_ui()
        self.init_my_page_functionality()

    def __iter__(self):
        root = self.get_root()
        reverse_pages = root._pages[::-1]
        return iter(reverse_pages)

    @final
    def init_my_page_ui(self) -> None:
        self.setLayout(self._scroll_layout)
        self._scroll_layout.addWidget(self._scroll_area)
        self._scroll_area.setWidget(self._container)
        self._container.setLayout(self._page_layout)
        self._page_layout.addLayout(self._nav_layout)
        self._nav_layout.addWidget(self._return_button)
        self._nav_layout.addStretch()
        self._nav_layout.addWidget(self._breadcrumb_text)
        self._page_layout.addWidget(self._content)
        self._content.setLayout(self._content_layout)

        self.in_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self._spiner.setHidden(False)

        self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._page_layout.setContentsMargins(0, 32, 8, 32)
        self._nav_layout.setContentsMargins(16, 0, 16, 16)
        self._content_layout.setContentsMargins(16, 0, 16, 0)

        self._scroll_area.setWidgetResizable(True)
        self._nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._return_button.setEnabled(False)

        self._scroll_area.setStyleSheet("border: none;")

    @final
    def init_my_page_functionality(self) -> None:
        # noinspection PyUnresolvedReferences
        self._return_button.clicked.connect(self.on_click_return_button)

    @final
    def get_root(self):
        root = self
        while root.prev_page is not None:
            root = root.prev_page
        return root

    @property
    def content(self) -> QFrame:
        return self._content

    @final
    def push_page(self, page, disable_return: bool = False) -> None:
        root = self.get_root()
        root._pages.append(page)
        self.states.prior_pages.append(page)
        item_to_hide = root._page_layout.itemAt(root._page_layout.count() - 1)
        widget_to_hide = item_to_hide.widget()
        widget_to_hide.setHidden(True)
        root._page_layout.addWidget(page.content)
        page_names = [page.page_name for page in root._pages]
        page_names.insert(0, root.page_name)
        root._breadcrumb_text.setText(' / '.join(page_names))
        if disable_return:
            root._return_button.setEnabled(False)
        else:
            root._return_button.setEnabled(True)

    @final
    @Slot()
    def pop_page(self) -> None:
        root = self.get_root()
        page_to_del = root._pages.pop()
        self.states.prior_pages.remove(page_to_del)
        item_to_del = root._page_layout.itemAt(root._page_layout.count() - 1)
        widget_to_del = item_to_del.widget()
        root._page_layout.removeItem(item_to_del)
        item_to_recover = root._page_layout.itemAt(root._page_layout.count() - 1)
        widget_to_recover = item_to_recover.widget()
        widget_to_recover.setHidden(False)
        widget_to_del.deleteLater()
        page_to_del.deleteLater()
        page_names = [page.page_name for page in root._pages]
        page_names.insert(0, root.page_name)
        root._breadcrumb_text.setText(' / '.join(page_names))
        if len(root._pages) == 0 or root.disable_further_return:
            root._return_button.setEnabled(False)
            root.disable_further_return = False

    def on_click_return_button(self) -> None:
        self.pop_page()

    @final
    def add_widget(
            self,
            widget: QWidget,
            alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
    ) -> None:
        self._content_layout.addWidget(widget, alignment=alignment)

    @final
    def add_layout(
            self,
            layout: QLayout,
            stretch: int = 0
    ) -> None:
        self._content_layout.addLayout(layout, stretch=stretch)

    @final
    def add_stretch(self, stretch: int = 0) -> None:
        self._content_layout.addStretch(stretch)

    @final
    def add_spacing(self, spacing: int) -> None:
        self._content_layout.addSpacing(spacing)

    @final
    def set_scroll_layout_padding(self, left: int, top: int, right: int, bottom: int) -> None:
        self._scroll_layout.setContentsMargins(left, top, right, bottom)

    @final
    def set_page_layout_padding(self, left: int, top: int, right: int, bottom: int) -> None:
        self._page_layout.setContentsMargins(left, top, right, bottom)

    @final
    def set_nav_layout_padding(self, left: int, top: int, right: int, bottom: int) -> None:
        self._nav_layout.setContentsMargins(left, top, right, bottom)

    @final
    def set_content_layout_padding(self, left: int, top: int, right: int, bottom: int) -> None:
        self._scroll_area.setContentsMargins(left, top, right, bottom)

    @final
    def set_disable_further_return(self, value: bool) -> None:
        root = self.get_root()
        root.disable_further_return = value

    def show_spiner(self):
        root = self.get_root()
        item_to_hide = root._page_layout.itemAt(root._page_layout.count() - 1)
        widget_to_hide = item_to_hide.widget()
        widget_to_hide.setHidden(True)
        root._page_layout.addWidget(
            self.in_progress_bar,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.in_progress_bar.setHidden(False)

    def hide_spiner(self):
        root = self.get_root()
        root._page_layout.removeWidget(self.in_progress_bar)
        root._page_layout.itemAt(root._page_layout.count() - 1).widget().setHidden(False)
        self.in_progress_bar.setHidden(True)

    @Slot()
    def update_info(self) -> None:
        pass
