from typing import List, Optional

from PySide6.QtWidgets import QApplication

from my_helpers import get_avatar_id


class FrontendStates:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self._prior_pages: List = []
        self._user_uuid: Optional[str] = None
        self._home_page = None
        self._search_page = None
        self._category_page = None
        self._user_page = None
        self._buttons = []

    def set_pages(
            self, *,
            home_page,
            search_page,
            category_page,
            user_page
    ):
        self._home_page = home_page
        self._search_page = search_page
        self._category_page = category_page
        self._user_page = user_page
        self.prior_pages.append(self._home_page)
        self.prior_pages.append(self._search_page)
        self.prior_pages.append(self._category_page)
        self.prior_pages.append(self._user_page)

    def login(self, user_uuid: str):
        self._user_uuid = user_uuid

    def logout(self):
        self._user_uuid = None
        self.update_info()

    @property
    def is_loggedin(self) -> bool:
        return self._user_uuid is not None

    @property
    def user_uuid(self) -> str:
        return self._user_uuid

    @property
    def avatar_id(self) -> int:
        return get_avatar_id(self.user_uuid)

    @property
    def prior_pages(self) -> List:
        return self._prior_pages

    @property
    def buttons(self) -> List:
        return self._buttons

    def update_info(self) -> None:
        for page in self.prior_pages[::-1]:
            QApplication.processEvents()
            print(f"通知页面 {page.page_name} 刷新 ui.")
            page.update_info()
