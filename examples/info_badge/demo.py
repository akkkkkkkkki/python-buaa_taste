# coding:utf-8
import sys

from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qmaterialwidgets import (InfoBadge, IconInfoBadge, setTheme, Theme, DotInfoBadge, PrimaryFloatingActionButton,
                            InfoBadgePosition, InfoBadgeManager)
from qmaterialwidgets import FluentIcon as MIC


@InfoBadgeManager.register('Custom')
class CustomInfoBadgeManager(InfoBadgeManager):
    """ Custom info badge manager """

    def position(self):
        pos = self.target.geometry().center()
        x = pos.x() - self.badge.width() // 2
        y = self.target.y() - self.badge.height() // 2
        return QPoint(x, y)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)

        self.vBoxLayout = QVBoxLayout(self)

        # info badge
        self.hBoxLayout1 = QHBoxLayout()
        self.hBoxLayout1.setSpacing(20)
        self.hBoxLayout1.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.hBoxLayout1.addStretch(1)
        self.hBoxLayout1.addWidget(InfoBadge.info(1))
        self.hBoxLayout1.addWidget(InfoBadge.success(10))
        self.hBoxLayout1.addWidget(InfoBadge.attension(100))
        self.hBoxLayout1.addWidget(InfoBadge.warning(1000))
        self.hBoxLayout1.addWidget(InfoBadge.error(10000))
        self.hBoxLayout1.addWidget(InfoBadge.custom('管理员', '#005fb8', '#60cdff'))
        self.hBoxLayout1.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout1)

        # dot info badge
        self.hBoxLayout2 = QHBoxLayout()
        self.hBoxLayout2.setSpacing(20)
        self.hBoxLayout2.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.hBoxLayout2.addStretch(1)
        self.hBoxLayout2.addWidget(DotInfoBadge.info())
        self.hBoxLayout2.addWidget(DotInfoBadge.success())
        self.hBoxLayout2.addWidget(DotInfoBadge.attension())
        self.hBoxLayout2.addWidget(DotInfoBadge.warning())
        self.hBoxLayout2.addWidget(DotInfoBadge.error())
        self.hBoxLayout2.addWidget(DotInfoBadge.custom('#005fb8', '#60cdff'))
        self.hBoxLayout2.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout2)

        # icon info badge
        self.hBoxLayout3 = QHBoxLayout()
        self.hBoxLayout3.setSpacing(20)
        self.hBoxLayout3.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.hBoxLayout3.addStretch(1)
        self.hBoxLayout3.addWidget(IconInfoBadge.info(MIC.ACCEPT_MEDIUM))
        self.hBoxLayout3.addWidget(IconInfoBadge.success(MIC.ACCEPT_MEDIUM))
        self.hBoxLayout3.addWidget(IconInfoBadge.attension(MIC.ACCEPT_MEDIUM))
        self.hBoxLayout3.addWidget(IconInfoBadge.warning(MIC.CANCEL_MEDIUM))
        self.hBoxLayout3.addWidget(IconInfoBadge.error(MIC.CANCEL_MEDIUM))

        badge = IconInfoBadge.custom(MIC.RINGER, '#005fb8', '#60cdff')
        badge.setFixedSize(32, 32)
        badge.setIconSize(QSize(16, 16))
        self.hBoxLayout3.addWidget(badge)

        self.hBoxLayout3.addStretch(1)
        self.vBoxLayout.addLayout(self.hBoxLayout3)

        # Using an InfoBadge in another control
        self.button = PrimaryFloatingActionButton(MIC.BASKETBALL, self)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignHCenter)
        InfoBadge.success(1, self, target=self.button, position=InfoBadgePosition.TOP_RIGHT)

        # NOTE: Use custom info badge manager
        # InfoBadge.success(1, self, target=self.button, position='Custom')

        self.resize(450, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()