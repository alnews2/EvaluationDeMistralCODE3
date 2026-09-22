"""Tests de la saisie clavier via de vrais QKeyEvent.

Contrairement aux autres tests d'IHM qui appellent directement ``_on_key``,
ces tests simulent des événements clavier complets pour couvrir
``keyPressEvent`` (mapping touches → actions, y compris les cas non mappés).
"""

from __future__ import annotations

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from calculator.ui.main_window import MainWindow


@pytest.fixture()
def window(qtbot) -> MainWindow:
    win = MainWindow()
    qtbot.addWidget(win)
    return win


def _press(window: MainWindow, key: Qt.Key, text: str = "") -> None:
    """Injecte un vrai QKeyEvent dans la fenêtre."""
    event = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier, text)
    window.keyPressEvent(event)


def test_saisie_clavier_complete(window: MainWindow) -> None:
    """12 + 34 = via le clavier physique uniquement."""
    _press(window, Qt.Key.Key_1, "1")
    _press(window, Qt.Key.Key_2, "2")
    _press(window, Qt.Key.Key_Plus, "+")
    _press(window, Qt.Key.Key_3, "3")
    _press(window, Qt.Key.Key_4, "4")
    _press(window, Qt.Key.Key_Return)
    assert window._display.text() == "46"  # noqa: SLF001


def test_operateurs_clavier(window: MainWindow) -> None:
    """Les touches / * - du pavé numérique mappent vers ÷ × −."""
    _press(window, Qt.Key.Key_6, "6")
    _press(window, Qt.Key.Key_Asterisk, "*")
    _press(window, Qt.Key.Key_7, "7")
    _press(window, Qt.Key.Key_Enter)
    assert window._display.text() == "42"  # noqa: SLF001
    _press(window, Qt.Key.Key_Escape)
    _press(window, Qt.Key.Key_9, "9")
    _press(window, Qt.Key.Key_Slash, "/")
    _press(window, Qt.Key.Key_0, "0")
    _press(window, Qt.Key.Key_Return)
    assert window._display.text() == "Erreur"  # noqa: SLF001


def test_backspace_et_minus_clavier(window: MainWindow) -> None:
    _press(window, Qt.Key.Key_5, "5")
    _press(window, Qt.Key.Key_7, "7")
    _press(window, Qt.Key.Key_Backspace)
    assert window._display.text() == "5"  # noqa: SLF001
    _press(window, Qt.Key.Key_Minus, "-")
    _press(window, Qt.Key.Key_2, "2")
    _press(window, Qt.Key.Key_Return)
    assert window._display.text() == "3"  # noqa: SLF001


def test_point_decimal_et_zero_initial_clavier(window: MainWindow) -> None:
    _press(window, Qt.Key.Key_Period, ".")
    _press(window, Qt.Key.Key_5, "5")
    assert window._display.text() == "0.5"  # noqa: SLF001
    # "0" puis "5" : remplacement du zéro initial
    _press(window, Qt.Key.Key_Escape)
    _press(window, Qt.Key.Key_0, "0")
    _press(window, Qt.Key.Key_5, "5")
    assert window._display.text() == "5"  # noqa: SLF001


def test_touche_non_mappee_est_ignoree(window: MainWindow) -> None:
    """Une touche sans action (ex. F1) ne doit rien casser."""
    _press(window, Qt.Key.Key_F1)
    _press(window, Qt.Key.Key_5, "5")
    assert window._display.text() == "5"  # noqa: SLF001
