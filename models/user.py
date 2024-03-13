from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from backend import (
    DishNotFound,
    user_add_favorite,
    user_get_uuids,
    user_login,
    user_record,
    user_register,
    user_remove_favorite,
    user_update_password,
    user_update_username,
    check_favorite,
    check_record,
    UsernameTaken,
    UserNotExist,
    UserNotFound,
    WrongPassword
)
from models.frontendstates import FrontendStates


class UserModel:
    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            username: Optional[str] = None,
            is_admin: Optional[bool] = None,
            recommend_dishes_uuids: Optional[List[str]] = None,
            records_uuids: Optional[List[str]] = None,
            favorite_dishes_uuids: Optional[List[str]] = None,
            favorite_counters_uuids: Optional[List[str]] = None,
    ):
        self.states: FrontendStates = states
        self.uuid: Optional[str] = uuid
        self.username: Optional[str] = username
        self.is_admin: Optional[bool] = is_admin
        self.recommend_dishes_uuids: Optional[List[str]] = recommend_dishes_uuids
        self.records_uuids: Optional[List[str]] = records_uuids
        self.favorite_dishes_uuids: Optional[List[str]] = favorite_dishes_uuids
        self.favorite_counters_uuids: Optional[List[str]] = favorite_counters_uuids

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        try:
            data = user_get_uuids(user_uuid=uuid)
            self.uuid = uuid
            self.username = data['username']
            self.is_admin = data['is_admin']
            self.recommend_dishes_uuids = data['recommend_dishes']
            self.records_uuids = data['records_uuids']
            self.favorite_dishes_uuids = data['favorite_dishes_uuids']
            self.favorite_counters_uuids = data['favorite_counters_uuids']
            return self
        except UserNotFound as e:
            raise e
        except UserNotExist as e:
            raise e

    @staticmethod
    def register(*, username: str, password: str, is_admin: bool):
        return user_register(
            username=username,
            password=password,
            is_admin=is_admin
        )

    def login(self, *, username: str, password: str):
        try:
            self.uuid = user_login(
                username=username,
                password=password
            )
            self.states.login(
                user_uuid=self.uuid
            )
            return self.fetch(uuid=self.uuid)
        except UserNotFound as e:
            raise e
        except WrongPassword as e:
            raise e

    def update_username(self, *, new_username: str):
        try:
            user_update_username(
                user_uuid=self.states.user_uuid,
                new_username=new_username
            )
            self.username = user_get_uuids(
                user_uuid=self.states.user_uuid
            )['username']
            if self.states is not None:
                self.states.update_info()
            return self
        except UserNotFound as e:
            raise e
        except UsernameTaken as e:
            raise e

    def update_password(self, *, new_password: str):
        try:
            user_update_password(
                user_uuid=self.states.user_uuid,
                new_password=new_password
            )
            return self
        except UserNotFound as e:
            raise e

    def add_record(self, *, dish_uuid: str, time: str):
        """返回记录的 UUID。"""
        try:
            user_record(
                user_uuid=self.states.user_uuid,
                dish_uuid=dish_uuid,
                time=time
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UserNotFound as e:
            raise e
        except DishNotFound as e:
            raise e

    def add_favorite(self, *, dish_uuid: str):
        try:
            user_add_favorite(
                user_uuid=self.states.user_uuid,
                dish_uuid=dish_uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UserNotFound as e:
            raise e
        except DishNotFound as e:
            raise e

    def remove_favorite(self, *, dish_uuid: str):
        try:
            user_remove_favorite(
                user_uuid=self.states.user_uuid,
                dish_uuid=dish_uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UserNotFound as e:
            raise e
        except DishNotFound as e:
            raise e
    
    def check_record(self, *, dish_uuid: str):
        return check_record(
            user_uuid=self.states.user_uuid,
            dish_uuid=dish_uuid
            )
    
    def check_favorite(self, *, dish_uuid: str):
        return check_favorite(
            user_uuid=self.states.user_uuid,
            dish_uuid=dish_uuid
        )

    @property
    def avatar(self) -> QPixmap:
        last_two_digits = int(self.uuid[-2:], 16)
        mapped_number = (last_two_digits % 29) + 1

        return (
            QPixmap(f":/avatars/{mapped_number}.png")
            .scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding
            )
        )
