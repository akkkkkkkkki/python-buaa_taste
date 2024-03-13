# 用于测试

import random
from typing import Tuple

from PySide6 import QtCore
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget

from components.tile import SimpleTile
from models.frontendstates import FrontendStates

# noinspection PyUnresolvedReferences
from resources import resources

cuisine_styles = [
    "川菜", "粤菜", "湘菜", "鲁菜", "浙菜", "苏菜", "闽菜", "徽菜", "东北菜", "西北菜",
    "江西菜", "北京菜", "上海菜", "新疆菜", "台湾菜", "云南菜", "西餐", "日本料理",
    "韩国料理", "泰国料理", "印度菜", "意大利菜", "法国菜", "墨西哥菜", "巴西菜"
]
chinese_dishes = [
    "香辣干锅鸡", "蒜香酱爆虾", "五香牛肉炒面", "蚝油炒时蔬", "麻辣鸡丝火锅", "蒸鲜肉包子",
    "香菇肉片炒饭", "麻辣牛肉拉面", "豉汁蒸鲈鱼", "糖醋里脊排骨", "葱姜蒸活鱼", "干煸四季豆",
    "香煎豆腐饼", "麻婆豆腐煲", "蒜蓉蒸扇贝", "醋溜白菜", "宫保鸡丁炒饭", "蚝油牛柳炒粉",
    "酸辣汤锅", "红烧狮子头"
]

restaurant_data = {
    "蓝天餐厅": "清新自然，让您尽情享受美味与美景。",
    "金牌烧烤": "炭火烧烤，肉质鲜嫩，满足您的味蕾。",
    "香榭饺子屋": "手工饺子，口味地道，回味无穷。",
    "海港海鲜馆": "新鲜海产，海鲜美食的天堂。",
    "川味醉香斋": "正宗川菜，辣味十足，挑战您的味蕾。",
    "橙园甜品屋": "甜品艺术，让您沉醉在甜蜜的世界。",
    "意大利风情": "浪漫意式风情，品味纯正的意大利美食。",
    "东方美味坊": "中式美食，传承经典，充满家的味道。",
    "素食禅心阁": "精心烹制素食，满足身心平衡。",
    "和风日式料理": "日本料理大师，带您领略和风美味。",
    "墨西哥烤肉": "墨西哥风情，烤肉火爆，辣而不失醇厚。",
    "山野采摘园": "绿色有机，采摘乐趣，尽享农家乐。",
    "泰香酸辣馆": "泰国风味，香辣刺激，开启味蕾冒险。",
    "渔家乐海鲜": "渔舟唱晚，品尝地道渔家海鲜。",
    "蜜糖甜蜜屋": "甜蜜滋味，浪漫缠绵，甜蜜时光。",
    "咖啡书香庄": "书香咖啡，惬意悠然，静享文艺时光。",
    "乡村野菜馆": "乡村风味，野菜美食，健康与口感兼得。",
    "寿司天堂": "寿司大师，鲜美绝伦，回味无穷。",
    "南洋风情屋": "南洋美食，异域风情，让您感受异国他乡。",
    "北方涮羊肉": "冬日涮肉，热辣过瘾，团聚共享欢乐时光。"
}

images = [
    'hamburger',
    'noodle',
    'vegetable',
    'steak',
    'cake',
    'gongbaojiding',
    'icecream'
]


def image_bytes(path: str) -> bytes:
    image = QImage(path)
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)
    image.save(buffer, "JPEG")
    return buffer.data()


def generate_image() -> bytes:
    dish_name = random.choice(images)
    return image_bytes(f':/images/{dish_name}')


def generate_dish_item(name=None) -> Tuple[QWidget, str]:
    return generate_simple_tile_item()


def generate_simple_tile_item() -> Tuple[SimpleTile, str]:
    name, description = random.choice(list(restaurant_data.items()))

    widget = SimpleTile(
        name=name,
        description=description + "SDFGVHBJNKNJNJHBGVFDGHBJNKHBVFGDXGHBJGFDGHBJBGHVFG",
        image=generate_image(),
        backend=None,
        states=FrontendStates()
    )

    return widget, name

def generate_avatar() -> bytes:
    return image_bytes(f':/avatars/{random.randint(1, 29)}.png')
