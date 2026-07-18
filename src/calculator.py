"""
Glassmorphism Calculator
A sleek, minimalist calculator built with PyQt6.

Author: Aljun Pagasi-an
License: MIT
"""

import sys
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt6.QtGui import (
    QColor, QPainter, QBrush, QFont, QLinearGradient, QPen
)


class GlassButton(QPushButton):
    """
    A custom glass-style button with hover and press animations.

    Features:
        - Opacity animation on hover (0.15 -> 0.35)
        - Scale animation on press/release (1.0 -> 0.92 -> 1.0 with elastic)
        - Three visual variants: default, accent (operators), danger (clear)
        - Drop shadow for depth
    """

    def __init__(
        self, 
        text: str, 
        parent: Optional[QWidget] = None, 
        accent: bool = False, 
        danger: bool = False, 
        wide: bool = False
    ) -> None:
        super().__init__(text, parent)
        self.accent = accent
        self.danger = danger
        self.wide = wide

        self._opacity = 0.15
        self._scale = 1.0

        self.setFixedSize(150 if wide else 70, 70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

        # Animations
        self.hover_anim = QPropertyAnimation(self, b"opacity")
        self.hover_anim.setDuration(200)
        self.hover_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.press_anim = QPropertyAnimation(self, b"scale")
        self.press_anim.setDuration(100)
        self.press_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.release_anim = QPropertyAnimation(self, b"scale")
        self.release_anim.setDuration(200)
        self.release_anim.setEasingCurve(QEasingCurve.Type.OutElastic)

        self.setStyleSheet("color: white; border: none; background: transparent;")

    # --- Properties for animations ---

    def get_opacity(self) -> float:
        return self._opacity

    def set_opacity(self, val: float) -> None:
        self._opacity = val
        self.update()

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    def get_scale(self) -> float:
        return self._scale

    def set_scale(self, val: float) -> None:
        self._scale = val
        self.update()

    scale = pyqtProperty(float, get_scale, set_scale)

    # --- Event handlers ---

    def enterEvent(self, event) -> None:
        self.hover_anim.setStartValue(self._opacity)
        self.hover_anim.setEndValue(0.35)
        self.hover_anim.start()
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.hover_anim.setStartValue(self._opacity)
        self.hover_anim.setEndValue(0.15)
        self.hover_anim.start()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self.press_anim.setStartValue(1.0)
        self.press_anim.setEndValue(0.92)
        self.press_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.release_anim.setStartValue(0.92)
        self.release_anim.setEndValue(1.0)
        self.release_anim.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Scale transform
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)

        rect = self.rect().adjusted(2, 2, -2, -2)

        # Color selection
        if self.accent:
            color = QColor(0, 150, 255, int(self._opacity * 255))
            border_color = QColor(100, 200, 255, 180)
        elif self.danger:
            color = QColor(255, 80, 80, int(self._opacity * 255))
            border_color = QColor(255, 150, 150, 180)
        else:
            color = QColor(255, 255, 255, int(self._opacity * 255))
            border_color = QColor(255, 255, 255, 120)

        painter.setBrush(QBrush(color))
        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 20, 20)

        # Text
        painter.setPen(QColor(255, 255, 255, 240))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()


class GlassDisplay(QLabel):
    """
    Custom glass-style display widget showing expression history and current value.

    Features:
        - Gradient glass background
        - Expression history (small text, top)
        - Current value (large text, bottom-right)
        - Drop shadow for depth
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(100)
        self.setFont(QFont("Segoe UI", 36, QFont.Weight.Light))
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("color: white; padding: 15px; background: transparent;")

        self._expression = ""
        self._current = "0"

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.shadow.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow)

    def update_display(self, expression: str, current: str) -> None:
        """Update the displayed expression and current value."""
        self._expression = expression
        self._current = current
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(4, 4, -4, -4)

        # Glass background gradient
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(255, 255, 255, 30))
        gradient.setColorAt(1, QColor(255, 255, 255, 10))

        painter.setBrush(QBrush(gradient))
        pen = QPen(QColor(255, 255, 255, 80))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 20, 20)

        # Expression text (small, top)
        painter.setPen(QColor(255, 255, 255, 160))
        painter.setFont(QFont("Segoe UI", 12))
        expr_rect = rect.adjusted(15, 8, -15, 0)
        painter.drawText(
            expr_rect, 
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, 
            self._expression
        )

        # Current value (large, bottom)
        painter.setPen(QColor(255, 255, 255, 240))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Light))
        val_rect = rect.adjusted(15, 25, -15, -8)
        painter.drawText(
            val_rect, 
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom, 
            self._current
        )

        painter.end()


class GlassCalculator(QMainWindow):
    """
    Main calculator window with glassmorphism design.

    Features:
        - Frameless, draggable window
        - Glass background with gradient glow
        - Custom glass buttons and display
        - Full calculator logic with expression evaluation
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(360, 580)

        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - 360) // 2, 
            (screen.height() - 580) // 2
        )

        # Calculator state
        self.expression = ""
        self.current = "0"
        self.reset_next = False
        self.last_was_op = False
        self.drag_pos: Optional[QPoint] = None

        # Build UI
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Initialize the user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title bar
        title = QLabel("Glassmorphism Calculator")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: rgba(255,255,255,0.7); padding: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Display
        self.display = GlassDisplay()
        layout.addWidget(self.display)

        # Button grid
        self._create_buttons(layout)

        # Window shadow
        self.window_shadow = QGraphicsDropShadowEffect(self)
        self.window_shadow.setBlurRadius(40)
        self.window_shadow.setColor(QColor(0, 0, 0, 120))
        self.window_shadow.setOffset(0, 10)
        central.setGraphicsEffect(self.window_shadow)

    def _create_buttons(self, layout: QVBoxLayout) -> None:
        """Create the calculator button grid."""
        buttons_data = [
            [("C", True, False, False), ("±", False, False, False), 
             ("%", False, False, False), ("÷", False, True, False)],
            [("7", False, False, False), ("8", False, False, False), 
             ("9", False, False, False), ("×", False, True, False)],
            [("4", False, False, False), ("5", False, False, False), 
             ("6", False, False, False), ("−", False, True, False)],
            [("1", False, False, False), ("2", False, False, False), 
             ("3", False, False, False), ("+", False, True, False)],
            [("0", False, False, True), (".", False, False, False), 
             ("=", False, True, False)],
        ]

        for row_data in buttons_data:
            hbox = QHBoxLayout()
            hbox.setSpacing(10)
            for text, danger, accent, wide in row_data:
                btn = GlassButton(text, accent=accent, danger=danger, wide=wide)
                btn.clicked.connect(lambda checked, t=text: self.on_button(t))
                hbox.addWidget(btn)
            layout.addLayout(hbox)

    def paintEvent(self, event) -> None:
        """Paint the main window glass background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(10, 10, -10, -10)

        # Outer glow
        glow = QLinearGradient(0, 0, rect.width(), rect.height())
        glow.setColorAt(0, QColor(100, 180, 255, 40))
        glow.setColorAt(0.5, QColor(180, 100, 255, 30))
        glow.setColorAt(1, QColor(255, 100, 180, 40))

        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect.adjusted(-5, -5, 5, 5), 30, 30)

        # Main body
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(20, 20, 40, 220))
        gradient.setColorAt(1, QColor(10, 10, 25, 235))

        painter.setBrush(QBrush(gradient))
        pen = QPen(QColor(255, 255, 255, 60))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 25, 25)

        # Top highlight line
        highlight = QLinearGradient(0, rect.top(), rect.width(), rect.top())
        highlight.setColorAt(0, QColor(255, 255, 255, 0))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 80))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(highlight, 2))
        painter.drawLine(
            rect.left() + 30, rect.top() + 1, 
            rect.right() - 30, rect.top() + 1
        )

        painter.end()

    def mousePressEvent(self, event) -> None:
        """Start window drag."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Handle window drag."""
        if self.drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        """End window drag."""
        self.drag_pos = None

    def on_button(self, text: str) -> None:
        """Handle button clicks."""
        if text == "C":
            self._clear()
        elif text == "±":
            self._toggle_sign()
        elif text == "%":
            self._percentage()
        elif text == "=":
            self._calculate()
        elif text in "+×÷−":
            self._operator(text)
        else:
            self._digit(text)

        self.update_display()

    def _clear(self) -> None:
        """Clear all state."""
        self.expression = ""
        self.current = "0"
        self.reset_next = False
        self.last_was_op = False

    def _toggle_sign(self) -> None:
        """Toggle positive/negative sign."""
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current

    def _percentage(self) -> None:
        """Convert current value to percentage."""
        try:
            val = float(self.current)
            self.current = str(val / 100)
        except (ValueError, ZeroDivisionError):
            pass

    def _calculate(self) -> None:
        """Evaluate the expression."""
        try:
            expr = self.expression + self.current
            expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
            result = eval(expr)
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(result)
            self.expression = ""
            self.reset_next = True
        except Exception:
            self.current = "Error"
            self.reset_next = True

    def _operator(self, text: str) -> None:
        """Handle operator buttons."""
        op_map = {"+": "+", "−": "-", "×": "*", "÷": "/"}
        if self.last_was_op:
            self.expression = self.expression[:-1] + op_map[text]
        else:
            self.expression += self.current + op_map[text]
        self.reset_next = True
        self.last_was_op = True

    def _digit(self, text: str) -> None:
        """Handle digit and decimal buttons."""
        if self.reset_next:
            self.current = text
            self.reset_next = False
        else:
            if self.current == "0" and text != ".":
                self.current = text
            elif text == "." and "." in self.current:
                pass
            else:
                self.current += text
        self.last_was_op = False

    def update_display(self) -> None:
        """Update the display widget."""
        expr = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.display.update_display(expr, self.current)


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    calc = GlassCalculator()
    calc.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
