import math

from PySide6.QtCore import (QSize, Qt, Signal)
from PySide6.QtWidgets import (QAbstractButton, QButtonGroup, QHBoxLayout, QLabel, QPushButton,
                               QSizePolicy, QWidget)

from my_helpers import load_icon
# noinspection PyUnresolvedReferences
from resources import resources


class StarRating(QWidget):
    """
    A custom widget for displaying and editing star ratings.

    This widget allows users to view and set star ratings.
    It displays five star-icons and allows partial ratings.
    The widget is editable if specified during initialization.

    Signals:
        rating_changed(float): Emitted when the rating is changed. The new rating is passed as an argument.

    """

    rating_changed = Signal(float)

    def __init__(
            self,
            rating=0.0,
            editable=False,
            show_number=True,
            show_divider=True,
            parent=None
    ):
        """
        Initialize the StarRating widget.

        Args:
            rating (float): The initial star rating (default is 0.0).
            parent (QWidget): The parent widget (default is None).
            editable (bool): Set to True to allow the user to edit the rating (default is False).
            show_divider (bool): Set to True to show the divider and the maximum rating value (default is True).

        """
        super(StarRating, self).__init__(parent)
        if rating > 5.0:
            self._rating = 5.0
        elif rating < 0.0:
            self._rating = 0.0
        else:
            self._rating = rating
        self._button_group = QButtonGroup()  # Button group for numbering the buttons
        self._show_number = show_number
        self._show_divider = show_divider
        if rating - math.floor(rating) > 0.01:  # Allow editing when the input rating is not an integer
            self._editable = False
        else:
            self._editable = editable

        # Connect the ratingChanged signal when editable
        if self._editable:
            self._button_group.buttonClicked[QAbstractButton].connect(self._on_clicked)

        # Set a fixed size for the widget
        # self.setFixedSize(240, 24)

        # Set up the horizontal layout
        layout = QHBoxLayout()
        layout.setSpacing(0)  # Set button spacing to 0
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # layout.addStretch(1)

        # Create five star-buttons
        for i in range(5):
            button = QPushButton()
            button.setIconSize(QSize(16, 16))  # Set the button size to 24 x 24
            button.setStyleSheet("border: none;")  # Remove button borders
            layout.addWidget(button)
            self._button_group.addButton(button, i + 1)

        # Add a fixed width space to maintain a distance of 10 pixels
        if self._show_number:
            layout.addSpacing(10)

        # Set appropriate icon resources for each button based on the rating value
        self._update_icons(self._rating)

        # Add a QLabel to display the rating
        if self._show_number:
            self._rating_label = QLabel()
            self._rating_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            layout.addWidget(self._rating_label)

            # layout.addStretch(1)

            # Update the rating text
            self._update_rating_label()

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def _update_icons(self, rating):
        """
        Update the star icons' display state.

        Args:
            rating (float): The star rating, including fractional values.

        """
        for i in range(5):
            button = self._button_group.button(i + 1)
            if i < math.floor(rating):  # Integer part of the rating
                button.setIcon(load_icon("star100"))
            elif i == math.floor(rating):  # Display partial stars
                partial_stars = rating - math.floor(rating)
                icon_name = f"star{int(partial_stars * 10) * 10}"
                button.setIcon(load_icon(icon_name))
            else:
                button.setIcon(load_icon("star0"))

    def _on_clicked(self, button):
        """
        Handle the star icon click event.

        Args:
            button (QAbstractButton): The clicked button.

        """
        if self._editable:
            rating = self._button_group.id(button)
            self.set_rating(rating)

    def get_rating(self):
        """
        Get the current star rating.

        Returns:
            float: The star rating.

        """
        return self._rating

    def set_rating(self, rating):
        """
        Set the star rating.

        Args:
            rating (float): The star rating.

        """
        button = self._button_group.button(rating)
        button.setChecked(True)
        self._rating = rating
        self._update_icons(rating)
        self._update_rating_label()
        self.rating_changed.emit(rating)

    def _update_rating_label(self):
        """
        Update the rating label.

        """
        if self._show_divider:
            self._rating_label.setText(f"{self._rating:.1f} / 5")
        else:
            self._rating_label.setText(f"{self._rating:.1f}")
