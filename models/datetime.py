from typing import Optional

from PySide6.QtCore import (
    QDate,
    QDateTime,
    QTime
)


class DateTimeModel:
    def __init__(
            self, *,
            date_time: Optional[QDateTime] = None
    ):
        self.date_time: Optional[QDateTime] = date_time

    def set_date(self, *, date: QDate):
        self.date_time.setDate(date)
        return self

    def set_time(self, *, time: QTime):
        self.date_time.setTime(time)
        return self

    def set_date_time(self, *, date_time: QDateTime):
        self.date_time = date_time
        return self

    def from_text(self, *, text: str):
        self.date_time = QDateTime.fromString(text, "yyyy-MM-dd hh:mm")
        return self

    def to_text(self) -> Optional[str]:
        if self.date_time is not None:
            return self.date_time.toString("yyyy-MM-dd hh:mm")
        else:
            return None

    @staticmethod
    def current_date_time_text() -> str:
        return QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
