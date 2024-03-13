from typing import Optional, Set

from PySide6.QtWidgets import QHBoxLayout, QWidget

from components.infobars import create_warning_info_bar
from models.canteen import CanteenModel
from models.counter import CounterModel
from models.frontendstates import FrontendStates
from qmaterialwidgets import (
    ComboBox,
    FluentIcon,
    TransparentToolButton
)
from components.mypage import MyPage


class CanteenCounterComboBoxes(QWidget):
    # noinspection PyUnresolvedReferences
    def __init__(
            self, *,
            states: FrontendStates,
            init_counter: Optional[CounterModel],
            selected_counters: Set[CounterModel],
            page: MyPage,
            parent=None
    ):
        super(CanteenCounterComboBoxes, self).__init__(parent)
        self.states: FrontendStates = states
        self.page: MyPage = page

        self.canteens: Optional[Dict[str, CanteenModel]] = None
        self.counters: Optional[Dict[str, CounterModel]] = None
        self.current_counter: Optional[CounterModel] = init_counter
        self.current_canteen: Optional[CanteenModel] = (
            CanteenModel().set_states(states=self.states).fetch(
                uuid=self.current_counter.canteen_uuid
            ) if init_counter is not None else None
        )
        self.selected_counters: Set[CounterModel] = selected_counters

        self.delete_button_func = None

        self.layout = QHBoxLayout()
        self.canteen_combobox = ComboBox()
        self.counter_combobox = ComboBox()
        self.delete_button = TransparentToolButton(FluentIcon.CLOSE, None)

        self.init_pair_ui()
        self.init_pair_func()
        self.init_counter_options()

    def init_pair_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.canteen_combobox)
        self.layout.addWidget(self.counter_combobox)
        self.layout.addStretch()
        self.layout.addWidget(self.delete_button)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canteen_combobox.setFixedWidth(250)
        self.counter_combobox.setFixedWidth(250)

    def init_pair_func(self):
        # noinspection PyUnresolvedReferences
        self.delete_button.clicked.connect(self.on_click_delete_button)
        self.canteen_combobox.currentTextChanged.connect(self.on_canteen_changed)
        self.counter_combobox.currentTextChanged.connect(self.on_counter_changed)

    def init_counter_options(self):
        self.canteen_combobox.clear()
        self.counter_combobox.clear()
        self.canteens = {
            canteen.name: canteen
            for canteen in CanteenModel.get_all(states=self.states)
        }

        self.canteen_combobox.addItems(self.canteens.keys())
        if self.current_canteen is not None:
            self.canteen_combobox.setCurrentText(
                self.current_canteen.name
            )
        else:
            self.canteen_combobox.setCurrentIndex(-1)

        counter_names = self.counter_names_generator()
        self.counter_combobox.addItems(counter_names)

        if self.current_counter is not None:
            self.counter_combobox.setCurrentText(
                self.current_counter.name
            )
        else:
            self.counter_combobox.setCurrentIndex(-1)

    def counter_names_generator(self):
        counters_list = [
            CounterModel()
            .set_states(states=self.states)
            .fetch(uuid=counter_uuid)
            for counter_uuid in self.current_canteen.counters_uuids
        ] if self.current_canteen is not None else []

        self.counters = {
            counter.name: counter
            for counter in counters_list
        }

        return self.counters.keys()

    def on_canteen_changed(self):
        self.current_canteen = self.canteens[self.canteen_combobox.text()]
        self.init_counter_options()

    def on_counter_changed(self):
        counter = self.counters[self.counter_combobox.text()]
        selected_counters_uuids = {
            counter.uuid
            for counter in self.selected_counters
        }
        if counter.uuid in selected_counters_uuids:
            create_warning_info_bar('该柜台已被添加。请勿重复添加。', parent=self.page.get_root())
            self.on_click_delete_button()
        else:
            if self.current_counter is not None:
                self.selected_counters.remove(self.current_counter)
            self.current_counter = self.counters[self.counter_combobox.text()]
            self.selected_counters.add(self.current_counter)

    def on_click_delete_button(self):
        self.selected_counters.discard(self.current_counter)
        print(self.selected_counters)
        self.delete_button_func()
