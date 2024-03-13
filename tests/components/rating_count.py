from PySide6.QtWidgets import QApplication

from components.rating_count import RatingCount


def test():
    app = QApplication()

    ratings = [0, 2, 3, 4, 25]
    rating_count = RatingCount(ratings)
    rating_count.show()

    app.exec()


if __name__ == '__main__':
    test()