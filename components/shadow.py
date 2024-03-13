from typing import final, Tuple

import PySide6
from PySide6.QtCore import Property, QEasingCurve, QObject, QPointF, QPropertyAnimation, Qt, Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget


def shadow_animation() -> Tuple[
    QGraphicsDropShadowEffect,
    QPropertyAnimation,
    QPropertyAnimation,
    QPropertyAnimation,
    QPropertyAnimation
]:
    shadow_effect = QGraphicsDropShadowEffect()
    show_shadow_animation = QPropertyAnimation(shadow_effect, b'color')
    hide_shadow_animation = QPropertyAnimation(shadow_effect, b'color')
    click_animation = QPropertyAnimation(shadow_effect, b'offset')
    release_animation = QPropertyAnimation(shadow_effect, b'offset')

    shadow_effect.setColor(QColor(0, 0, 0, 0))
    shadow_effect.setBlurRadius(20)
    shadow_effect.setOffset(0, 4)
    show_shadow_animation.setEndValue(QColor(0, 0, 0, 25))
    show_shadow_animation.setDuration(100)
    hide_shadow_animation.setEndValue(QColor(0, 0, 0, 0))
    hide_shadow_animation.setDuration(100)
    click_animation.setEndValue(QPointF(0, 6))
    click_animation.setDuration(50)
    release_animation.setEndValue(QPointF(0, 4))
    release_animation.setDuration(50)

    return (shadow_effect,
            show_shadow_animation,
            hide_shadow_animation,
            click_animation,
            release_animation)


class ShadowAnimation:
    clicked = Signal(Qt.MouseButton)
    released = Signal(Qt.MouseButton)
    mouse_hover_changed = Signal(bool)

    def __init__(self, parent=None):
        super(ShadowAnimation, self).__init__(parent)
        self._mouse_hover = False
        (self.shadow_effect,
         self.show_shadow_animation,
         self.hide_shadow_animation,
         self.click_animation,
         self.release_animation) = shadow_animation()

        self.init_shadow_effect_functionality()

    def init_shadow_effect_functionality(self) -> None:
        self.clicked.connect(self.on_click)
        self.released.connect(self.release_animation.start)
        self.mouse_hover_changed.connect(self.hover_animation_control)

    @Property(bool)
    def mouse_hover(self):
        return self._mouse_hover

    @mouse_hover.setter
    def mouse_hover(self, state):
        if self._mouse_hover != state:
            self._mouse_hover = state
            self.mouse_hover_changed.emit(state)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.clicked.emit(event.button())

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.released.emit(event.button())

    def enterEvent(self, e):
        self.mouse_hover = True

    def leaveEvent(self, e):
        self.mouse_hover = False

    @final
    @Slot(bool)
    def hover_animation_control(self, hovered):
        if hovered:
            self.show_shadow_animation.start()
        else:
            self.hide_shadow_animation.start()

    @Slot()
    def on_click(self) -> None:
        self.click_animation.start()

    def apply_effect(self, target: QWidget) -> None:
        target.setGraphicsEffect(self.shadow_effect)


class FadeAnimation(QObject):
    def __init__(self, parent=None):
        super(FadeAnimation, self).__init__(parent)
        self._opacity = 1.0
        self.animation_duration = 500  # Duration of the animation in milliseconds

    @Property(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        if self._opacity != value:
            self._opacity = value
            self.target_widget.setWindowOpacity(value)

    def fade_in(self):
        self._start_animation(1.0)

    def fade_out(self):
        self._start_animation(0.0)

    def _start_animation(self, target_opacity):
        self.animation = QPropertyAnimation(self, b'opacity')
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.setStartValue(self._opacity)
        self.animation.setEndValue(target_opacity)
        self.animation.start()

    def apply_effect(self, target: QWidget) -> None:
        self.target_widget = target
        target.setWindowOpacity(self._opacity)
