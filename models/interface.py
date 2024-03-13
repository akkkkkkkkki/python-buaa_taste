from abc import ABC, abstractmethod

from models.frontendstates import FrontendStates


class CommentInterface(ABC):
    @abstractmethod
    def set_states(self, *, states: FrontendStates):
        pass

    @abstractmethod
    def fetch(self, *, uuid: str):
        pass

    @abstractmethod
    def like(self):
        pass

    @abstractmethod
    def cancel_like(self):
        pass

    @abstractmethod
    def dislike(self):
        pass

    @abstractmethod
    def cancel_dislike(self):
        pass

    @abstractmethod
    def reply(self, *, content: str):
        pass

    @abstractmethod
    def delete(self):
        pass
