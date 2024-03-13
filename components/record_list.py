from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QSizePolicy, QVBoxLayout, QWidget)

from components.layout import MonotoneList
from components.list_text_item import ListItem, TextItem
from components.mycard import MyCard
from components.mypage import MyPage
from models.dish import DishModel
from models.frontendstates import FrontendStates
from models.records import RecordModel
from models.user import UserModel
from qmaterialwidgets import (MessageBox, ScrollArea, TitleLabel)


class RecordView(QWidget):

    def __init__(self,
                 states: FrontendStates,
                 at_page: MyPage,
                 parent: QWidget = None):
        super(RecordView, self).__init__(parent)
        self.states = states
        self.current_page = at_page
        self.user_model = (
            UserModel()
            .set_states(states=states)
        )

        self.layout = QVBoxLayout(self)

        self.title_label = TitleLabel('管理历史记录', None)

        self.init_record_view_ui()
        self.init_record_view_func()

    def init_record_view_ui(self) -> None:
        self.setLayout(self.layout)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.setSpacing(40)
        self.layout.setContentsMargins(50, 50, 50, 50)

    def init_record_view_func(self) -> None:
        pass

    def update_info(self):
        if self.states.is_loggedin:
            while self.layout.count() > 1:
                item = self.layout.itemAt(1)
                widget = item.widget()
                self.layout.removeItem(item)
                widget.deleteLater()
            self.user_model.fetch(uuid=self.states.user_uuid)
            records: List[RecordModel] = [
                RecordModel()
                .set_states(states=self.states)
                .fetch(uuid=record_uuid)
                for record_uuid in self.user_model.records_uuids
            ]
            for record_model in records:
                dish_model = (
                    DishModel()
                    .set_states(states=self.states)
                    .fetch(uuid=record_model.dish_uuid)
                )
                list_item = ListItem(widget=TextItem(
                    main_text=dish_model.name,
                    secondary_text=record_model.time.to_text()
                ))
                list_item.delete_button.clicked.connect(
                    self.make_delete_func(record_model)
                )
                list_item.setFixedHeight(64)
                list_item.setFixedWidth(420)
                list_item.setContentsMargins(0, 0, 0, 0)
                self.layout.addWidget(list_item)

    def make_delete_func(self, record_model: RecordModel):
        def delete_func():
            message = MessageBox(
                '确定要删除吗？', '', self.current_page.get_root()
            )
            if message.exec():
                self.current_page.show_spiner()
                record_model.delete()
                self.current_page.hide_spiner()

        return delete_func
