from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from qmaterialwidgets import BodyLabel, CaptionLabel, DisplayLabel, ImageLabel, LargeTitleLabel, ScrollArea, \
    StrongBodyLabel, \
    SubtitleLabel, \
    TitleLabel

# noinspection PyUnresolvedReferences
from resources import resources


class LabelView(QWidget):
    def __init__(self, parent=None):
        super(LabelView, self).__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)

    def addLabel(self, label: QLabel):
        self.vBoxLayout.addWidget(label)


if __name__ == '__main__':
    app = QApplication([])

    scroll_area = ScrollArea()
    widget = LabelView()
    scroll_area.setWidget(widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumSize(400, 400)

    widget.addLabel(CaptionLabel('CaptionLabel 注脚', widget))
    widget.addLabel(BodyLabel('BodyLabel 正文', widget))
    widget.addLabel(StrongBodyLabel('StrongBodyLabel 粗体正文', widget))
    widget.addLabel(SubtitleLabel('SubtitleLabel 副标题', widget))
    widget.addLabel(TitleLabel('TitleLabel 标题', widget))
    widget.addLabel(LargeTitleLabel('LargeTitleLabel 大标题', widget))
    widget.addLabel(DisplayLabel('DisplayLabel 超大显示', widget))
    image = ImageLabel(f":/icons/star100", widget)
    image.setFixedSize(16, 16)
    widget.addLabel(image)

    # scroll_area.resize(400, 600)

    scroll_area.show()
    app.exec()