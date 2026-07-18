"""
Unit tests for the Glassmorphism Calculator.
"""

import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# We need a QApplication for Qt tests
app = QApplication(sys.argv)

from src.calculator import GlassCalculator, GlassButton, GlassDisplay


class TestCalculatorLogic:
    """Tests for calculator computation logic."""

    def setup_method(self):
        """Create fresh calculator instance for each test."""
        self.calc = GlassCalculator()

    def test_initial_state(self):
        """Test calculator starts with 0."""
        assert self.calc.current == "0"
        assert self.calc.expression == ""
        assert self.calc.reset_next is False

    def test_digit_input(self):
        """Test digit button handling."""
        self.calc.on_button("5")
        assert self.calc.current == "5"

        self.calc.on_button("3")
        assert self.calc.current == "53"

    def test_clear(self):
        """Test clear button resets state."""
        self.calc.on_button("5")
        self.calc.on_button("C")
        assert self.calc.current == "0"
        assert self.calc.expression == ""

    def test_addition(self):
        """Test basic addition."""
        self.calc.on_button("5")
        self.calc.on_button("+")
        self.calc.on_button("3")
        self.calc.on_button("=")
        assert self.calc.current == "8"

    def test_subtraction(self):
        """Test basic subtraction."""
        self.calc.on_button("9")
        self.calc.on_button("−")
        self.calc.on_button("4")
        self.calc.on_button("=")
        assert self.calc.current == "5"

    def test_decimal(self):
        """Test decimal input."""
        self.calc.on_button("1")
        self.calc.on_button(".")
        self.calc.on_button("5")
        assert self.calc.current == "1.5"

    def test_percentage(self):
        """Test percentage conversion."""
        self.calc.on_button("5")
        self.calc.on_button("0")
        self.calc.on_button("%")
        assert self.calc.current == "0.5"

    def test_toggle_sign(self):
        """Test sign toggle."""
        self.calc.on_button("5")
        self.calc.on_button("±")
        assert self.calc.current == "-5"
        self.calc.on_button("±")
        assert self.calc.current == "5"

    def test_error_handling(self):
        """Test division by zero error."""
        self.calc.on_button("5")
        self.calc.on_button("÷")
        self.calc.on_button("0")
        self.calc.on_button("=")
        assert self.calc.current == "Error"


class TestGlassButton:
    """Tests for GlassButton widget."""

    def test_button_creation(self):
        """Test button initializes correctly."""
        btn = GlassButton("Test")
        assert btn.text() == "Test"
        assert btn.accent is False
        assert btn.danger is False

    def test_accent_button(self):
        """Test accent button variant."""
        btn = GlassButton("+", accent=True)
        assert btn.accent is True

    def test_danger_button(self):
        """Test danger button variant."""
        btn = GlassButton("C", danger=True)
        assert btn.danger is True


class TestGlassDisplay:
    """Tests for GlassDisplay widget."""

    def test_display_update(self):
        """Test display content updates."""
        display = GlassDisplay()
        display.update_display("5 + 3", "8")
        assert display._expression == "5 + 3"
        assert display._current == "8"
