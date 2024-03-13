from typing import List

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from components.star_rating import StarRating


class RatingCount(QWidget):

    def __init__(self,
                 points_list: List[int] = None,
                 parent=None):
        if points_list is None or len(points_list) == 0:
            points_list = [0, 0, 0, 0, 0]

        super(RatingCount, self).__init__(parent)

        main_layout = QVBoxLayout()

        for i in range(5, 0, -1):
            line_layout = QHBoxLayout()

            stars = StarRating(rating=i, editable=False, show_number=False)
            line_layout.addWidget(stars)

            line_layout.addSpacing(10)
            count_label = QLabel(f"{points_list[i - 1]} 人评分")
            count_label.setStyleSheet("color: #a6a6a6")
            line_layout.addWidget(count_label)

            main_layout.addLayout(line_layout)

        self.setLayout(main_layout)


# Test code
