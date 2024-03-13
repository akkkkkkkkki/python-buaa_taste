from typing import List, Optional

from backend import (
    canteen_add,
    canteen_delete,
    canteen_get_all_ids,
    canteen_get_by_uuid,
    canteen_modify,
    canteen_search,
    CanteenNotExist,
    CanteenNotFound,
    UnauthorizedAccess
)
from models.frontendstates import FrontendStates
from models.image import ImageModel
from models.models import Models


class CanteenModel:
    states = FrontendStates()
    models = Models()

    def __init__(self, *, uuid: Optional[str] = None, name: Optional[str] = None, image_uuid: Optional[str] = None,
                 available: Optional[bool] = None, description: Optional[str] = None,
                 counters_uuids: Optional[List] = None):
        self.uuid: Optional[str] = uuid
        self.name: Optional[str] = name
        self.image_uuid: Optional[str] = image_uuid
        self.available: Optional[bool] = available
        self.description: Optional[str] = description
        self.counters_uuids: Optional[List[str]] = counters_uuids

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    @staticmethod
    def get(uuid: str):
        models = Models()
        if uuid in models.canteens:
            return models.canteens[uuid]
        else:
            try:
                info = canteen_get_by_uuid(uuid=uuid)
                model = CanteenModel(
                    uuid=info['uuid'],
                    name=info['name'],
                    image_uuid=info['image_uuid'],
                    available=info['available'],
                    description=info['description'],
                    counters_uuids=info['counters_uuids']
                )
                models.canteens[uuid] = model
                return model
            except CanteenNotExist as e:
                raise e

    @staticmethod
    def update(uuid: str):
        info = canteen_get_by_uuid(uuid=uuid)
        model = CanteenModel.get(uuid)
        model.name = info['name']
        model.image_uuid = info['image_uuid']
        model.available = info['available']
        model.description = info['description']
        model.counters_uuids = info['counters_uuids']

    def fetch(self, *, uuid: str):
        try:
            info = canteen_get_by_uuid(uuid=uuid)
            self.uuid = info['uuid']
            self.name = info['name']
            self.image_uuid = info['image_uuid']
            self.available = info['available']
            self.description = info['description']
            self.counters_uuids = info['counters_uuids']
            return self
        except CanteenNotExist as e:
            raise e

    @staticmethod
    def get_all(*, states: FrontendStates):
        uuids = canteen_get_all_ids()
        return [
            CanteenModel()
            .set_states(states=states)
            .fetch(uuid=canteen_uuid)
            for canteen_uuid in uuids
        ]

    @staticmethod
    def search(*, states: FrontendStates, keyword: str):
        uuids = canteen_search(keyword=keyword)
        return [
            CanteenModel()
            .set_states(states=states)
            .fetch(uuid=canteen_uuid)
            for canteen_uuid in uuids
        ]

    @staticmethod
    def add(
            *,
            states: FrontendStates,
            name: str,
            description: str,
            image: ImageModel
    ):
        try:
            canteen_uuid = canteen_add(
                user_uuid=states.user_uuid,
                name=name,
                description=description,
                image=image.data
            )
            if states is not None:
                states.update_info()
            return (
                CanteenModel()
                .set_states(states=states)
                .fetch(uuid=canteen_uuid)
            )
        except UnauthorizedAccess as e:
            raise e

    def modify(
            self, *,
            name: str,
            description: str,
            image: ImageModel
    ):
        try:
            canteen_modify(
                user_uuid=self.states.user_uuid,
                canteen_uuid=self.uuid,
                name=name,
                description=description,
                image=image.data
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UnauthorizedAccess as e:
            raise e
        except CanteenNotFound as e:
            raise e

    def delete(self):
        try:
            canteen_delete(
                user_uuid=self.states.user_uuid,
                canteen_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return None
        except UnauthorizedAccess as e:
            raise e
        except CanteenNotFound as e:
            raise e
