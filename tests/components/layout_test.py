from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from components.layout import MyGridView, MyListView
from generator import generate_dish_item
from qmaterialwidgets import ScrollArea


def test_list(*, orientation: Qt.Orientation, limit: int) -> None:
    app = QApplication([])

    main_widget = QWidget()
    main_layout = QVBoxLayout()

    # 文本输入框，提供给删除或添加用的 UUID
    line_edit = QLineEdit()
    main_layout.addWidget(line_edit)

    buttons_area = QHBoxLayout()
    del_button = QPushButton("删除")
    buttons_area.addWidget(del_button)
    add_button = QPushButton("添加至末尾")
    buttons_area.addWidget(add_button)
    unshift_button = QPushButton("添加至开头")
    buttons_area.addWidget(unshift_button)
    clear_button = QPushButton("清空")
    buttons_area.addWidget(clear_button)
    show_button = QPushButton("显示全部")
    buttons_area.addWidget(show_button)
    main_layout.addLayout(buttons_area)

    # 把列表放到滚动区域里面
    scroll_area = ScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    scroll_area.setStyleSheet("border: none;")

    list = MyListView(orientation=orientation, limit=limit)

    # 生成初始数据
    for i in range(5):
        dish_widget, dish_name = generate_dish_item()
        list.add_widget(dish_widget, dish_name)
    scroll_area.setWidget(list)
    main_layout.addWidget(scroll_area)
    # main_layout.addStretch()

    # 删除输入框对应的菜名 / UUID 的列表项
    def test_del():
        uuid = line_edit.text()
        list.remove_widget(uuid)
    del_button.clicked.connect(test_del)

    # 以输入框的内容为 UUID / 菜名生成加到列表底部
    def test_add():
        uuid = line_edit.text()
        widget_to_add, _ = generate_dish_item(uuid)
        list.add_widget(widget_to_add, uuid)
    add_button.clicked.connect(test_add)

    # 以输入框的内容为 UUID / 菜名生成加到列表顶上
    def test_unshift():
        uuid = line_edit.text()
        widget_to_add, _ = generate_dish_item(uuid)
        list.unshift_widget(widget_to_add, uuid)
    unshift_button.clicked.connect(test_unshift)

    # 清空列表
    def test_clear():
        list.clear()
    clear_button.clicked.connect(test_clear)

    # 测试限制显示个数
    if not list.is_limited():
        show_button.setEnabled(False)

    def test_show():
        if show_button.text() == "显示全部":
            list.set_limit(0)
            show_button.setText(f"限制显示{limit}个")
        else:
            list.set_limit(limit)
            show_button.setText("显示全部")
    show_button.clicked.connect(test_show)

    main_widget.setLayout(main_layout)
    main_widget.show()
    app.exec()


def test_grid(
        orientation: Qt.Orientation = Qt.Orientation.Vertical,
        generate_num: int = 30,
        line_num: int = 2,
        limit: int = 0
) -> None:
    app = QApplication([])

    main_widget = QFrame()
    main_layout = QVBoxLayout()

    # 文本输入框，提供给删除或添加用的 UUID
    line_edit = QLineEdit()
    # main_layout.addWidget(line_edit)

    buttons_area = QHBoxLayout()
    del_button = QPushButton("删除")
    buttons_area.addWidget(del_button)
    add_button = QPushButton("添加至末尾")
    buttons_area.addWidget(add_button)
    unshift_button = QPushButton("添加至开头")
    buttons_area.addWidget(unshift_button)
    clear_button = QPushButton("清空")
    buttons_area.addWidget(clear_button)
    show_button = QPushButton("显示全部")
    buttons_area.addWidget(show_button)
    main_layout.addLayout(buttons_area)

    grid = MyGridView(
        orientation=orientation,
        line_num=line_num,
        limit=limit
    )
    for i in range(generate_num):
        dish_widget, dish_name = generate_dish_item()
        grid.add_widget(dish_widget, dish_name)
    scroll_area = ScrollArea()
    scroll_area.setWidget(grid)
    scroll_area.setContentsMargins(0, 10, 0, 10)
    scroll_area.setWidgetResizable(True)
    scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    scroll_area.setStyleSheet("border: 0px")
    main_layout.addWidget(scroll_area)
    main_layout.addStretch()

    def test_del():
        uuid = line_edit.text()
        grid.remove_widget(uuid)
    del_button.clicked.connect(test_del)

    # 以输入框的内容为 UUID / 菜名生成加到列表底部
    def test_add():
        uuid = line_edit.text()
        widget_to_add, _ = generate_dish_item(uuid)
        grid.add_widget(widget_to_add, uuid)
    add_button.clicked.connect(test_add)

    # 以输入框的内容为 UUID / 菜名生成加到列表顶上
    def test_unshift():
        uuid = line_edit.text()
        widget_to_add, _ = generate_dish_item(uuid)
        grid.unshift_widget(widget_to_add, uuid)
    unshift_button.clicked.connect(test_unshift)

    # 清空列表
    def test_clear():
        grid.clear()
    clear_button.clicked.connect(test_clear)

    # 测试限制显示个数
    if not grid.is_limited():
        show_button.setEnabled(False)

    def test_show():
        if show_button.text() == "显示全部":
            grid.set_limit(0)
            show_button.setText(f"限制显示{limit}个")
        else:
            grid.set_limit(limit)
            show_button.setText("显示全部")
    show_button.clicked.connect(test_show)

    main_widget.setLayout(main_layout)
    main_widget.show()
    app.exec()


if __name__ == '__main__':
    test_grid(
        orientation=Qt.Orientation.Horizontal,
        line_num=3,
        generate_num=20,
        limit=0
    )
