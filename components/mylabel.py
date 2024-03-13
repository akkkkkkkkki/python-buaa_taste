from components.mycolor import MyColor
from qmaterialwidgets import CaptionLabel, LargeTitleLabel, StrongBodyLabel, SubtitleLabel, TitleLabel


class BoldBodyLabel(StrongBodyLabel):
    def __init__(self, text: str):
        super(BoldBodyLabel, self).__init__(text)
        font = self.getFont()
        font.setBold(True)
        self.setFont(font)


class BoldSubtitleLabel(SubtitleLabel):
    def __init__(self, text: str):
        super(BoldSubtitleLabel, self).__init__(text)
        font = self.getFont()
        font.setBold(True)
        self.setFont(font)


class BoldTitleLabel(TitleLabel):
    def __init__(self, text: str):
        super(BoldTitleLabel, self).__init__(text)
        font = self.getFont()
        font.setBold(True)
        self.setFont(font)


class SecondaryLabel(CaptionLabel):
    def __init__(self, text: str):
        super(SecondaryLabel, self).__init__(text)
        self.setTextColor(MyColor.GREY600.value)


class BoldLargeTitleLabel(LargeTitleLabel):
    def __init__(self, text: str):
        super(BoldLargeTitleLabel, self).__init__(text)
        font = self.getFont()
        font.setBold(True)
        self.setFont(font)
