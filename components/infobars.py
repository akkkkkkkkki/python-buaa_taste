from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from qmaterialwidgets import FluentIcon, InfoBar, InfoBarPosition


def create_info_bar(title: str, content: str, parent: QWidget) -> None:
    info_bar = InfoBar(
        icon=FluentIcon.INFO,
        title=title,
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent
    )
    info_bar.show()


def create_success_info_bar(content: str, parent: QWidget) -> None:
    info_bar = InfoBar.success(
        title='成功',
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent
    )
    info_bar.show()


def create_error_info_bar(content: str, parent: QWidget) -> None:
    info_bar = InfoBar.error(
        title='错误',
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent
    )
    info_bar.show()


def create_warning_info_bar(content: str, parent: QWidget) -> None:
    info_bar = InfoBar.warning(
        title='警告',
        content=content,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP_RIGHT,
        duration=3000,
        parent=parent
    )
    info_bar.show()


def create_alert(title: str, description: str, parent: QWidget) -> None:
    alert = InfoBar.error(
        title=title,
        content=description,
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=parent
    )
    alert.show()
