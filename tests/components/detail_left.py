from PySide6.QtWidgets import QApplication

from components.detail_left import LeftDetail

if __name__ == "__main__":
    app = QApplication([])

    name = "宫保鸡丁"
    img_url = ":/images/gongbaojiding"
    counter = "xx食堂xx窗口"
    score_num = [43, 23, 34, 54, 45]
    tags = ["正餐", "川菜"]
    price = 8.50
    rating = 4.7
    description = "这是宫保鸡丁"

    widget = LeftDetail(name, tags, counter, score_num, img_url, price, rating, description)
    widget.show()

    app.exec()
