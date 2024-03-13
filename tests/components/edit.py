from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget

from components.edit import PasswordEdit

if __name__ == '__main__':
    app = QApplication([])
    layout = QHBoxLayout()
    layout.addWidget(QLabel("密码"))
    layout.addWidget(PasswordEdit())
    window = QWidget()
    window.setLayout(layout)
    window.show()
    app.exec()
