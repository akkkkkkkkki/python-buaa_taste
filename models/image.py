from typing import Optional

from PySide6.QtCore import QBuffer, QByteArray
from PySide6.QtGui import (
    QImage,
    QPixmap
)

from backend import image_get_by_uuid
from models.frontendstates import FrontendStates


class ImageModel:
    def __init__(
            self, *,
            states: Optional[FrontendStates] = None,
            uuid: Optional[str] = None,
            data: Optional[bytes] = None
    ):
        self.states: Optional[FrontendStates] = states
        self.uuid: Optional[str] = uuid
        self.data: Optional[bytes] = data

    def set_states(self, *, states: FrontendStates):
        self.states = states
        return self

    def fetch(self, *, uuid: str):
        self.uuid = uuid
        self.data = image_get_by_uuid(uuid=uuid)
        return self

    def from_image(self, *, image: QImage):
        self.data = image.bits()
        return self.resize()

    def from_pixmap(self, *, pixmap: QPixmap):
        self.data = pixmap.toImage().bits()
        return self

    def from_data(self, data: bytes):
        self.data = data
        return self

    def to_image(self) -> Optional[QImage]:
        if self.data is not None:
            return QImage.fromData(self.data)
        else:
            return None

    def to_pixmap(self) -> Optional[QPixmap]:
        if self.data is not None:
            image = self.to_image()
            return QPixmap.fromImage(image)
        else:
            return None

    def resize(self):
        if self.data is not None:
            pixmap = self.to_pixmap()
            if pixmap.height() > 1024:
                pixmap = pixmap.scaledToHeight(1024)
                if pixmap.width() > 1024:
                    pixmap = pixmap.scaledToWidth(1024)
                    byte_array = QByteArray()
                    buffer = QBuffer(byte_array)
                    buffer.open(QBuffer.WriteOnly)
                    pixmap.save(buffer, "JPEG")
                    buffer.close()
                    self.data = byte_array.data()
        return self
