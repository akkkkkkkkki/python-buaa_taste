import math
from typing import Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QBoxLayout, QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget)


class MyListView(QWidget):
    def __init__(
            self, *,
            orientation: Qt.Orientation = Qt.Orientation.Vertical,
            limit: int = 0,
            parent=None
    ):
        super(MyListView, self).__init__(parent)
        self.widgets: Dict[str, QWidget] = {}
        self.orientation = orientation
        self.limit = limit if limit > 0 else 0
        self.layout = QVBoxLayout() if orientation == Qt.Orientation.Vertical else QHBoxLayout()

        self.init_ui()

    def init_ui(self) -> None:
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def rerender(self) -> None:
        if self.limit == 0:
            show_num = self.layout.count()
        else:
            show_num = min(self.layout.count(), self.limit)
        for i in range(show_num):
            self.layout.itemAt(i).widget().setHidden(False)
        for i in range(show_num, self.layout.count()):
            self.layout.itemAt(i).widget().setHidden(True)

    def add_widget(self, widget: QWidget, uuid: str) -> None:
        if uuid not in self.widgets:
            self.widgets[uuid] = widget
            self.layout.addWidget(widget)
            self.rerender()

    def add_widgets(self, widgets: Dict[str, QWidget]) -> None:
        for uuid, widget in widgets:
            if uuid not in self.widgets:
                self.widgets[uuid] = widget
                self.layout.addWidget(widget)
        self.rerender()

    def unshift_widget(self, widget: QWidget, uuid: str) -> None:
        if uuid not in self.widgets:
            self.widgets[uuid] = widget
            self.layout.insertWidget(0, widget)
            self.rerender()

    def remove_widget(self, uuid: str) -> None:
        if uuid in self.widgets:
            widget_to_del = self.widgets[uuid]
            self.layout.removeWidget(widget_to_del)
            widget_to_del.deleteLater()
            del (self.widgets[uuid])
            self.rerender()

    def clear(self) -> None:
        self.widgets.clear()
        while self.layout.count() > 0:
            item_to_del = self.layout.takeAt(0)
            widget_to_del = item_to_del.widget()
            if widget_to_del is not None:
                self.layout.removeItem(item_to_del)
                widget_to_del.deleteLater()

    def set_limit(self, limit: int) -> None:
        self.limit = limit if limit >= 0 else self.limit
        self.rerender()

    def is_limited(self) -> bool:
        return self.limit > 0

    def limit(self) -> int:
        return self.limit

    def set_spacing(self, spacing: int) -> None:
        self.layout.setSpacing(spacing)

    def setContentsMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self.layout.setContentsMargins(left, top, right, bottom)


class MyGridView(QWidget):
    def __init__(
            self, *,
            orientation: Qt.Orientation = Qt.Orientation.Vertical,
            line_num: int = 2,
            limit: int = 0,
            parent: Optional[QWidget] = None
    ):
        super(MyGridView, self).__init__(parent)
        self.orientation = orientation
        self.line_num = line_num
        self._limit = limit if limit > 0 else 0
        self.limit_line_count = math.ceil(limit / line_num)
        self.lines: List[QBoxLayout] = []
        self.widgets_dict: Dict[str, QWidget] = {}
        self.widgets_seq: List[QWidget] = []
        self.layout = QHBoxLayout() if orientation == Qt.Orientation.Vertical else QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        for i in range(self.line_num):
            if self.orientation == Qt.Orientation.Vertical:
                line = QVBoxLayout()
                line.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            else:
                line = QHBoxLayout()
                line.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
            line.setContentsMargins(0, 0, 0, 0)
            self.lines.append(line)
            self.layout.addLayout(line)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def clear(self, true_delete: bool = True) -> None:
        for line in self.lines:
            while line.count() > 0:
                item = line.itemAt(0)
                widget = item.widget()
                line.removeWidget(widget)
                if true_delete:
                    widget.deleteLater()
                else:
                    widget.setHidden(True)
        if true_delete:
            self.widgets_dict.clear()
            self.widgets_seq.clear()

    def rerender(self) -> None:
        self.clear(true_delete=False)
        if self._limit > 0:
            count = min(len(self.widgets_dict), self._limit)
        else:
            count = len(self.widgets_dict)
        for i in range(count):
            line = self.lines[i % self.line_num]
            widget = self.widgets_seq[i]
            line.addWidget(widget)
            widget.setHidden(False)

    def add_widget(self, widget: QWidget, uuid: str) -> None:
        if uuid not in self.widgets_dict:
            self.widgets_dict[uuid] = widget
            self.widgets_seq.append(widget)
            self.rerender()

    def add_widgets(self, widgets: Dict[str, QWidget]) -> None:
        for uuid, widget in widgets.items():
            if uuid not in self.widgets_dict:
                self.widgets_dict[uuid] = widget
                self.widgets_seq.append(widget)
        self.rerender()

    def unshift_widget(self, widget: QWidget, uuid: str) -> None:
        if uuid not in self.widgets_dict:
            self.widgets_dict[uuid] = widget
            self.widgets_seq.insert(0, widget)
            self.rerender()

    def remove_widget(self, uuid: str) -> None:
        if uuid in self.widgets_dict:
            widget = self.widgets_dict[uuid]
            del (self.widgets_dict[uuid])
            self.widgets_seq.remove(widget)
            self.rerender()

    def set_limit(self, limit: int) -> None:
        if limit >= 0:
            self._limit = limit
            self.rerender()

    def is_limited(self) -> bool:
        return self._limit > 0

    def limit(self) -> int:
        return self._limit

    def set_spacing(self, value: int) -> None:
        self.layout.setSpacing(value)
        for line in self.lines:
            line.setSpacing(value)


class MonotoneList(QWidget):
    def __init__(
            self, *,
            orientation: Qt.Orientation = Qt.Orientation.Vertical,
            limit: int = 0,
            parent=None
    ):
        super(MonotoneList, self).__init__(parent)
        self.orientation = orientation
        self.limit = limit if limit > 0 else 0
        self.layout = QVBoxLayout() if orientation == Qt.Orientation.Vertical else QHBoxLayout()

        self.init_ui()

    def init_ui(self) -> None:
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def add_widget(self, widget: QWidget, uuid: str) -> None:
        if self.count < self.limit:
            print(f'增加了组件 {uuid}')
        self.layout.addWidget(widget)

    def add_widgets(self, widgets: Dict[str, QWidget]) -> None:
        for uuid, widget in widgets:
            if self.count < self.limit:
                self.layout.addWidget(widget)
                print(f'增加了组件 {uuid}')

    def clear(self) -> None:
        while self.count > 0:
            item_to_del = self.layout.takeAt(0)
            widget_to_del = item_to_del.widget()
            if widget_to_del is not None:
                self.layout.removeItem(item_to_del)
                widget_to_del.deleteLater()

    @property
    def count(self) -> int:
        return self.layout.count()


class MonotoneGrid(QWidget):
    def __init__(
            self, *,
            orientation: Qt.Orientation = Qt.Orientation.Vertical,
            line_num: int = 2,
            limit: int = 0,
            parent: Optional[QWidget] = None
    ):
        super(MonotoneGrid, self).__init__(parent)
        self.orientation = orientation
        self.line_num = line_num
        self._limit = limit if limit > 0 else 0
        self.lines: List[QBoxLayout] = []
        self.widget_to_add: Optional[QWidget] = None
        self.layout = QHBoxLayout() if orientation == Qt.Orientation.Vertical else QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        for i in range(self.line_num):
            if self.orientation == Qt.Orientation.Vertical:
                line = QVBoxLayout()
                line.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            else:
                line = QHBoxLayout()
                line.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
            line.setContentsMargins(0, 0, 0, 0)
            self.lines.append(line)
            self.layout.addLayout(line)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def clear(self) -> None:
        for line in self.lines:
            while line.count() > 0:
                item = line.itemAt(0)
                widget = item.widget()
                line.removeWidget(widget)
                widget.deleteLater()

    def arrange(self) -> None:
        index = self.count
        line = self.lines[index % self.line_num]
        widget = self.widget_to_add
        line.addWidget(widget)
        widget.setHidden(False)

    def add_widget(self, widget: QWidget) -> None:
        if self.limit == 0 or self.count < self.limit:
            self.widget_to_add = widget
            self.arrange()

    @property
    def count(self) -> int:
        count = 0
        for line in self.lines:
            count += line.count()
        return count

    @property
    def limit(self) -> int:
        return self._limit
