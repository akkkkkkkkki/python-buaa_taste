from typing import List, Optional

from backend import (
    comment_delete,
    comment_dislike,
    comment_dislike_cancel,
    comment_get_by_uuid,
    comment_like,
    comment_like_cancel,
    comment_reply,
    CommentNotExist
)
from models.datetime import DateTimeModel
from models.frontendstates import FrontendStates
from models.image import ImageModel


class CommentModel:
    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            user_uuid: Optional[str] = None,
            is_main: Optional[bool] = None,
            available: Optional[bool] = None,
            time: Optional[DateTimeModel] = None,
            title: Optional[str] = None,
            rating: Optional[float] = None,
            content: Optional[str] = None,
            image: Optional[ImageModel] = None,
            like_count: Optional[int] = None,
            liked: Optional[bool] = None,
            dislike_count: Optional[int] = None,
            disliked: Optional[bool] = None,
            replies_uuids: Optional[List[str]] = None
    ):
        self.states: Optional[FrontendStates] = states
        self.uuid: Optional[str] = uuid
        self.user_uuid: Optional[str] = user_uuid
        self.is_main: Optional[bool] = is_main
        self.available: Optional[bool] = available
        self.time: Optional[DateTimeModel] = time
        self.title: Optional[str] = title
        self.rating: Optional[float] = rating
        self.content: Optional[str] = content
        self.image: Optional[ImageModel] = image
        self.like_count: Optional[int] = like_count
        self.liked: Optional[bool] = liked
        self.dislike_count: Optional[int] = dislike_count
        self.disliked: Optional[bool] = disliked
        self.replies_uuids: Optional[List[str]] = replies_uuids

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        try:
            if self.states is not None and self.states.is_loggedin:
                data = comment_get_by_uuid(
                    comment_uuid=uuid,
                    user_uuid=self.states.user_uuid
                )
                self.uuid = uuid
                self.is_main = data['is_main']
                self.user_uuid = data['user_uuid']
                self.available = data['available']
                self.time = (
                    DateTimeModel()
                    .from_text(text=data['time'])
                )
                self.title = data['title']
                self.rating = data['rating']
                self.content = data['content']
                self.image = (
                    ImageModel()
                    .set_states(states=self.states)
                    .fetch(uuid=data['image_uuid'])
                )
                self.like_count = data['like_count']
                self.liked = data['liked']
                self.dislike_count = data['dislike_count']
                self.disliked = data['disliked']
                self.replies_uuids = data['replies_uuids']
                return self
        except CommentNotExist as e:
            raise e

    def like(self):
        try:
            comment_like(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except CommentNotExist as e:
            raise e

    def cancel_like(self):
        try:
            comment_like_cancel(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except CommentNotExist as e:
            raise e

    def dislike(self):
        try:
            comment_dislike(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except CommentNotExist as e:
            raise e

    def cancel_dislike(self):
        try:
            comment_dislike_cancel(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except CommentNotExist as e:
            raise e

    def reply(self, *, content: str):
        try:
            comment_reply(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid,
                time=DateTimeModel.current_date_time_text(),
                content=content
            )
            if self.states is not None:
                self.states.update_info()
            return self.fetch(uuid=self.uuid)
        except CommentNotExist as e:
            raise e

    def delete(self):
        try:
            comment_delete(
                user_uuid=self.states.user_uuid,
                comment_uuid=self.uuid
            )
            if self.states is not None:
                self.states.update_info()
            return None
        except CommentNotExist as e:
            raise e
