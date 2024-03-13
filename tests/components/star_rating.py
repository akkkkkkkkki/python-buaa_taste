import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from components.star_rating import StarRating


def on_rating_changed(rating):
    print(f'New rating: {rating}')


def main():
    app = QApplication(sys.argv)

    # Create a vertical layout to hold the StarRating widgets
    layout = QVBoxLayout()

    # Create 5 StarRating widgets and add them to the layout
    for i in range(6):
        star_rating = StarRating(rating=i, show_number=False, editable=True, show_divider=True)
        star_rating.rating_changed.connect(on_rating_changed)
        layout.addWidget(star_rating)

    # Create a main widget to hold the vertical layout
    main_widget = QWidget()
    main_widget.setLayout(layout)

    # Set a fixed size for the main widget (optional)
    # main_widget.setFixedSize(250, 300)

    main_widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
