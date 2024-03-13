from typing import List, Optional

from PySide6.QtCore import QDateTime

from backend import (
    dish_add,
    dish_comment,
    dish_delete,
    dish_get_all_uuids,
    dish_get_by_uuid,
    dish_modify,
    dish_most_popular,
    dish_search,
    dish_top_rated,
    DishNotFound,
    UnauthorizedAccess
)
from models.frontendstates import FrontendStates
from models.image import ImageModel


class DishModel:
    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            available: Optional[bool] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            price: Optional[float] = None,
            image_uuid: Optional[str] = None,
            tags: Optional[List[str]] = None,
            counters_uuids: Optional[List[str]] = None,
            rating_average: Optional[float] = None,
            ratings: Optional[List[int]] = None,
            comments_uuids: Optional[List[str]] = None
    ):
        self.states: Optional[FrontendStates] = states
        self.uuid: Optional[str] = uuid
        self.available: Optional[bool] = available
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.price: Optional[float] = price
        self.image_uuid: Optional[str] = image_uuid
        self.tags: Optional[List[str]] = tags
        self.counters_uuids: Optional[List[str]] = counters_uuids
        self.rating_average: Optional[float] = rating_average
        self.ratings: Optional[List[int]] = ratings
        self.comments_uuids: Optional[List[str]] = comments_uuids

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        try:
            data = dish_get_by_uuid(uuid=uuid)
            self.uuid = uuid
            self.available = data['available']
            self.name = data['name']
            self.description = data['description']
            self.price = data['price']
            self.image_uuid = data['image_uuid']
            self.tags = data['tags']
            self.counters_uuids = data['counters_uuids']
            self.rating_average = data['rating_average']
            self.ratings = data['ratings']
            self.comments_uuids = data['comments_ids']
            return self
        except DishNotFound as e:
            raise e

    @staticmethod
    def get_all_dishes(*, states: FrontendStates):
        try:
            all_uuids = dish_get_all_uuids()
            return [
                DishModel()
                .set_states(states=states)
                .fetch(uuid=dish_uuid)
                for dish_uuid in all_uuids
            ]
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def search(*, states: FrontendStates, keyword: str):
        uuids = dish_search(keyword=keyword)
        return [
            DishModel()
            .set_states(states=states)
            .fetch(uuid=dish_uuid)
            for dish_uuid in uuids
        ]

    @staticmethod
    def add(
            *,
            states: FrontendStates,
            name: str,
            description: str,
            price: float,
            image: ImageModel,
            tags: List[str],
            counters_uuids: List[str]
    ):
        try:
            dish_uuid = dish_add(
                user_uuid=states.user_uuid,
                name=name,
                description=description,
                price=price,
                image=image.data,
                tags=tags,
                counters_uuids=counters_uuids
            )
            if states is not None:
                states.update_info()
            return (
                DishModel()
                .set_states(states=states)
                .fetch(uuid=dish_uuid)
            )
        except UnauthorizedAccess as e:
            raise e

    def modify(
            self, *,
            name: str,
            description: str,
            price: float,
            image: ImageModel,
            tags: List[str],
            counters_uuids: List[str]
    ):
        try:
            dish_modify(
                user_uuid=self.states.user_uuid,
                dish_uuid=self.uuid,
                name=name,
                description=description,
                price=price,
                image=image.data,
                tags=tags,
                counters=counters_uuids
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UnauthorizedAccess as e:
            raise e
        except DishNotFound as e:
            raise e

    def delete(self):
        try:
            dish_delete(
                user_uuid=self.states.user_uuid,
                dish_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return None
        except UnauthorizedAccess as e:
            raise e
        except DishNotFound as e:
            raise e

    def add_comment(
            self, *,
            title: str,
            content: str,
            rating: float,
            image: Optional[ImageModel]
    ):
        """会返回新增评论的 UUID"""
        try:
            comment_uuid = dish_comment(
                user_uuid=self.states.user_uuid,
                dish_uuid=self.uuid,
                time=QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm"),
                title=title,
                content=content,
                rating=rating,
                image=image.data if image is not None else None
            )
            if self.states is not None:
                self.states.update_info()
            return comment_uuid
        except DishNotFound as e:
            raise e

    @staticmethod
    def get_most_popular(*, states: FrontendStates):
        uuids = dish_most_popular()
        return [
            DishModel()
            .set_states(states=states)
            .fetch(uuid=dish_uuid)
            for dish_uuid in uuids
        ]

    @staticmethod
    def get_top_rated(*, states: FrontendStates):
        uuids = dish_top_rated()
        return [
            DishModel()
            .set_states(states=states)
            .fetch(uuid=dish_uuid)
            for dish_uuid in uuids
        ]
