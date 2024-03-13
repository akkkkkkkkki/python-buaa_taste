from typing import Optional

from backend import (
    CanteenNotExist,
    counter_add,
    counter_delete,
    counter_get_all,
    counter_get_by_uuid,
    counter_modify,
    counter_search,
    CounterNotExist,
    UnauthorizedAccess
)
from models.frontendstates import FrontendStates
from models.image import ImageModel


class CounterModel:

    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            name: Optional[str] = None,
            image_uuid: Optional[str] = None,
            available: Optional[bool] = None,
            description: Optional[str] = None,
            canteen_uuid: Optional[str] = None,
    ):
        self.states: Optional[FrontendStates] = states
        self.uuid: Optional[str] = uuid
        self.name: Optional[str] = name
        self.image_uuid: Optional[str] = image_uuid
        self.available: Optional[bool] = available
        self.description: Optional[str] = description
        self.canteen_uuid: Optional[str] = canteen_uuid

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        try:
            info = counter_get_by_uuid(uuid=uuid)
            self.uuid = uuid
            self.name = info['name']
            self.available = info['available']
            self.description = info['description']
            self.image_uuid = info['image_uuid']
            self.canteen_uuid = info['canteen_uuid']
            return self
        except CounterNotExist as e:
            raise e

    @staticmethod
    def get_all(*, states: FrontendStates):
        uuids = counter_get_all()
        return [
            CounterModel()
            .set_states(states=states)
            .fetch(uuid=counter_uuid)
            for counter_uuid in uuids
        ]

    @staticmethod
    def search(*, states: FrontendStates, keyword: str):
        uuids = counter_search(keyword=keyword)
        return [
            CounterModel()
            .set_states(states=states)
            .fetch(uuid=counter_uuid)
            for counter_uuid in uuids
        ]

    @staticmethod
    def add(
            *,
            states: FrontendStates,
            name: str,
            canteen=None,
            description: str,
            image: ImageModel
    ):
        try:
            counter_uuid = counter_add(
                user_uuid=states.user_uuid,
                name=name,
                canteen_uuid=canteen.uuid,
                description=description,
                image=image.data
            )
            if states is not None:
                states.update_info()
            return (
                CounterModel()
                .set_states(states=states)
                .fetch(uuid=counter_uuid)
            )
        except UnauthorizedAccess as e:
            raise e

    def modify(
            self, *,
            name: str,
            canteen=None,
            description: str,
            image: ImageModel
    ):
        try:
            counter_modify(
                user_uuid=self.states.user_uuid,
                counter_uuid=self.uuid,
                name=name,
                canteen_uuid=canteen.uuid,
                description=description,
                image=image.data
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except UnauthorizedAccess as e:
            raise e
        except CounterNotExist as e:
            raise e
        except CanteenNotExist as e:
            raise e

    def delete(self):
        try:
            counter_delete(
                user_uuid=self.states.user_uuid,
                counter_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return None
        except UnauthorizedAccess as e:
            raise e
        except CounterNotExist as e:
            raise e
