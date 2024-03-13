from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from backend import user_get_uuids
from components.mycolor import MyColor
from components.mylabel import BoldSubtitleLabel
from models.frontendstates import FrontendStates
from models.user import UserModel
from my_helpers import load_avatar
from qmaterialwidgets import BodyLabel, ImageLabel, InfoBadge


class UserInfo(QWidget):
    def __init__(self,
                 user_model: UserModel,
                 states: FrontendStates,
                 parent=None):
        super(UserInfo, self).__init__(parent)
        self.states = states
        self.user_model = user_model

        self.layout = QVBoxLayout()

        self.avatar_label = ImageLabel(load_avatar(1))
        self.name_label = BoldSubtitleLabel('用户名')
        self.admin_label = InfoBadge.success('管理员')
        self.record_label = BodyLabel('记录过 n 次 ｜ 收藏了 m 道菜品', None)

        self.init_user_info_ui()

    def init_user_info_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.admin_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.record_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(15)

        self.record_label.setStyleSheet(f'color: {MyColor.GREY600.value};')

    def update_info(self) -> None:
        if self.states.is_loggedin:
            self.user_model.fetch(uuid=self.user_model.uuid)
            self.avatar_label.setPixmap(self.user_model.avatar)
            self.name_label.setText(self.user_model.username)
            if self.user_model.is_admin:
                self.admin_label.setVisible(True)
            else:
                self.admin_label.setVisible(False)
            self.record_label.setText(
                f"记录过 {len(self.user_model.records_uuids)} 次 | "
                f"收藏 {len(self.user_model.favorite_dishes_uuids)} 道菜品"
            )
