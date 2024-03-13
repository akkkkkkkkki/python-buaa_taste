from enum import Enum

from PySide6.QtGui import QIcon

from qmaterialwidgets import getIconColor, MaterialIconBase, Theme
# noinspection PyUnresolvedReferences
from resources import resources


class MyIcon(MaterialIconBase, Enum):
    """ Custom icons """

    DISLIKE = "Dislike"
    LIKE = "Like"
    EYE = "Eye"
    EYEOFF = "EyeOff"

    def path(self, theme=Theme.AUTO):
        return f':/icons/{self.value}_{getIconColor(theme)}.svg'

    def qicon(self, theme=Theme.AUTO):
        return QIcon(self.path())
