from typing import Optional

from backend import (
    record_delete,
    record_get_by_uuid,
    RecordNotFound
)
from models.frontendstates import FrontendStates
from models.datetime import DateTimeModel


class RecordModel:
    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            dish_uuid: Optional[str] = None,
            time: Optional[DateTimeModel] = None
    ):
        self.states: Optional[FrontendStates] = states
        self.uuid: Optional[str] = uuid
        self.dish_uuid: Optional[str] = dish_uuid
        self.time: Optional[DateTimeModel] = time

    def set_states(self, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        try:
            data = record_get_by_uuid(uuid=uuid)
            self.uuid = uuid
            self.dish_uuid = data['dish_uuid']
            self.time = DateTimeModel().from_text(text=data['time'])
            return self
        except RecordNotFound as e:
            raise e

    def delete(self):
        try:
            record_delete(
                uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return None
        except RecordNotFound as e:
            raise e
