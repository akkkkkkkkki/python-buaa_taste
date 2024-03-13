from PySide6.QtWidgets import QApplication

from components.comment import CommentItem
from models.frontendstates import FrontendStates
from generator import generate_avatar
from tests.components.TestWindow import MyTestWindow

comment_uuid = '1a07e7ef-b00d-4ba4-a74a-d0c804cd7115'
username = "张三"
avatar = generate_avatar()
time = "2023-07-24 10:30"
title = '学校宫保鸡丁不错！学校宫保鸡丁不错！学校宫保鸡丁不错！'
content = "宫保鸡丁的外观令人赏心悦目。金黄的鸡丁与翠绿的葱段、红亮的辣椒交相辉映，" \
              "构成了一幅色彩斑斓的美食画面。精心制作的鸡丁均匀切割，大小适中，" \
              "每一块都饱含着浓郁的鸡肉香气。宫保鸡丁是一道集色香味俱佳的美食佳肴。" \
              "它不仅仅是满足味蕾的享受，" \
              "更是对中国传统烹饪艺术的传承与创新。无论是与亲朋好友共聚一堂，" \
              "还是在繁忙的生活中寻求一份美味的慰藉，宫保鸡丁都是您最好的选择。" \
              "尽情享受这道美味，让您的味蕾感受中华美食的魅力！"
rating = 4.0
likes = 10
liked = True
dislikes = 2
disliked = False
replies = 5
states = FrontendStates()
backend = None

if __name__ == "__main__":
    app = QApplication([])
    window = MyTestWindow(800, 500)
    widget = CommentItem(
        comment_uuid,
        username,
        avatar,
        time,
        title,
        content,
        rating,
        likes,
        liked,
        dislikes,
        disliked,
        replies,
        states,
        backend,
        None
    )
    window.add_widget(widget)
    app.exec()
