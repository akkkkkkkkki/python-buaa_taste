from PySide6.QtWidgets import QApplication

from components.user import Login


def test_login_submit(username: str, password: str) -> None:
    print("登录：")
    print(f"用户名：{username}")
    print(f"密码：{password}")


def test_register_submit(username: str, password: str) -> None:
    print("注册：")
    print(f"用户名：{username}")
    print(f"密码：{password}")


def test_login() -> None:
    app = QApplication([])
    window = Login(
        login_func=test_login_submit,
        register_func=test_register_submit,
        is_register=False,
    )
    window.setWindowTitle("登录")
    window.show()
    app.exec()


if __name__ == "__main__":
    test_login()
