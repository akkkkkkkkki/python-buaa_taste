from typing import Any, Dict


class Models:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self._canteens: Dict[str, Any] = {}
        self._comments: Dict[str, Any] = {}
        self._counters: Dict[str, Any] = {}
        self._dishes: Dict[str, Any] = {}
        self._images: Dict[str, Any] = {}
        self._records: Dict[str, Any] = {}
        self._users: Dict[str, Any] = {}

    @property
    def canteens(self):
        return self._canteens

    @property
    def comments(self):
        return self._comments

    @property
    def counters(self):
        return self._counters

    @property
    def dishes(self):
        return self._dishes

    @property
    def images(self):
        return self._images

    @property
    def records(self):
        return self._records

    @property
    def users(self):
        return self._users
