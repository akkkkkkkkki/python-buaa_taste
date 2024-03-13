from typing import List, Optional

import password_strength
from password_strength import PasswordPolicy
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap

# noinspection PyUnresolvedReferences
from resources import resources


# 菜系列表

# 中餐名字列表


def load_icon(resource_name):
    """
    Load an icon from the resource file.

    Args:
        resource_name (str): The name of the icon in the resource file.

    Returns:
        QIcon: The loaded icon's QIcon. Returns an empty QIcon if loading fails.

    """
    file = QFile(f":/icons/{resource_name}")
    if file.open(QIODevice.ReadOnly):
        data = file.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        return icon
    return QIcon()


def load_avatar(index: int):
    return (QPixmap(f":/avatars/{index}.png")
            .scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding))


def truncate_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 1] + '…'


def bytes_to_pixmap(buf: bytes) -> QPixmap:
    image = QImage().fromData(buf)
    return QPixmap(image)


def crop_scale(pixmap: QPixmap, width: int, height: int) -> QPixmap:
    return pixmap.scaled(
        width,
        height,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding
    )


def check_password_strength(password) -> Optional[str]:
    # 创建密码策略
    policy = PasswordPolicy.from_names(
        length=8,  # 最小长度为8
        numbers=1,  # 至少包含一个数字
        uppercase=1,  # 至少包含一个大写字母
        special=1,  # 至少包含一个特殊字符
    )

    # 评估密码强度
    failed_conditions = policy.test(password)

    # 返回密码强度结果
    if failed_conditions:
        message = ""

        for condition in failed_conditions:
            if isinstance(condition, password_strength.tests.Length):
                message += "\n密码长度应大于 8 位。"
            elif isinstance(condition, password_strength.tests.Special):
                message += '\n至少包含一个特殊字符。'
            elif isinstance(condition, password_strength.tests.Numbers):
                message += '\n至少包含一个数字。'
            elif isinstance(condition, password_strength.tests.Uppercase):
                message += '\n至少包含一个大写字符。'

        return message
    else:
        return None


def check_username(username: str) -> Optional[str]:
    messages: List[str] = []
    # 用户名长度必须在2到8个字符之间
    if not 2 <= len(username) <= 8:
        messages.append("用户名长度必须在 2 到 8 个字符之间。")

    # 只能包含字母（大小写均可）、数字和下划线
    if any(char.isspace() for char in username):
        messages.append("不能包含空白字符。")

    if len(messages) > 0:
        return "\n".join(messages)
    else:
        return None


def get_avatar_id(user_uuid: str) -> int:
    last_two_digits = int(user_uuid[-2:], 16)
    mapped_number = (last_two_digits % 29) + 1
    return mapped_number
