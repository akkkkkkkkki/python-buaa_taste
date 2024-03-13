import os

from PySide6 import QtCore
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QWidget

from components.infobars import (
    create_success_info_bar,
    create_info_bar,
    create_error_info_bar
)


def upload_image(self):
    options = QFileDialog.Option.ReadOnly

    file_name, _ = QFileDialog.getOpenFileName(
        self,
        "选择图片",
        "",
        "图像类型 (*.png *.jpeg *.jpg *.bmp);;所有类型 (*)",
        options=options)

    if file_name:
        pixmap = QPixmap(file_name)
        image = QImage(file_name)
        byte_array = QByteArray()
        buffer = QtCore.QBuffer(byte_array)
        buffer.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "JPEG")
        buffer.close()
        bytes_data = byte_array.data()
        self.image_uuid = bytes_data
        self.image_label.setPixmap(pixmap.scaled(100, 100))


def open_image_file(parent: QWidget) -> bytes:
    try:
        user_home_dir = os.path.expanduser("~")

        file_path, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption="选择图片",
            dir=user_home_dir,
            filter="图像类型 (*.png *.jpeg *.jpg *.bmp);;所有类型 (*)",
            options=QFileDialog.Option.ReadOnly
        )

        if file_path:
            with open(file_path, "rb") as file:
                content = file.read()
                create_success_info_bar(content='成功打开了文件。', parent=parent)
                return content
        else:
            create_info_bar(title='提示', content='没有打开任何文件。', parent=parent)
    except Exception as e:
        create_error_info_bar(content=f'遇到错误 {str(e)}。', parent=parent)

    return b''
