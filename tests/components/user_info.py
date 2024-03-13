import random
import sys

from PySide6.QtWidgets import QApplication

from components.user_info import UserInfo

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = UserInfo("爱吃鱼香肉丝", str(random.randint(1, 29)), '23', '12', '93')
    widget.show()

    sys.exit(app.exec())