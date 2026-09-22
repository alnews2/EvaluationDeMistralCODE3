"""Fenêtre principale de la calculatrice.

L'interface est volontairement séparée de la logique métier (``calculator.core``) :
elle se contente de traduire les actions de l'utilisateur en appels au moteur,
et affiche soit le résultat, soit un message d'erreur.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from calculator.core import Calculator, Operation, format_number, operation_from_symbol

_ERROR_MESSAGE = "Erreur"

_STYLE = """
QMainWindow { background: #1e1f24; }
QLineEdit {
    font-size: 32px;
    padding: 16px;
    border-radius: 8px;
    background: #2b2d36;
    color: #f5f6fa;
    text-align: right;
}
QPushButton {
    font-size: 20px;
    min-width: 56px;
    min-height: 56px;
    border: none;
    border-radius: 8px;
    background: #3a3d4a;
    color: #f5f6fa;
}
QPushButton:hover { background: #4a4e5e; }
QPushButton:pressed { background: #2b2d36; }
QPushButton#btnEquals { background: #4f8cff; }
QPushButton#btnEquals:hover { background: #6b9dff; }
QPushButton#btnClear, QPushButton#btnBack {
    background: #e0566b; color: #ffffff;
}
"""

# Symboles des touches : None = case vide (fusionnée par le code de layout)
_KEYS: list[list[str | None]] = [
    ["C", "⌫", "÷", "×"],
    ["7", "8", "9", "−"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", None],  # "=" fusionné verticalement sur 2 lignes
    ["0", ".", "="],
]

_DIGITS = set("0123456789.")
_OPERATOR_SYMBOLS = {op.value for op in Operation}


class MainWindow(QMainWindow):
    """Fenêtre principale : afficheur + pavé de touches."""

    def __init__(self) -> None:
        super().__init__()
        self._calc = Calculator()
        self._acc: float | None = None
        self._pending_op: Operation | None = None
        self._current = "0"
        self._fresh_entry = True
        self._error = False

        self.setWindowTitle("QuatreOps — Calculatrice")
        self.setMinimumSize(320, 420)
        self._build_ui()
        self.setStyleSheet(_STYLE)
        self._refresh_display()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        self._display = QLineEdit()
        self._display.setReadOnly(True)
        self._display.setMaxLength(40)
        root.addWidget(self._display)

        pad = QWidget()
        grid = QGridLayout(pad)
        grid.setSpacing(8)
        buttons: dict[str, QPushButton] = {}
        equals_btn: QPushButton | None = None

        for row, keys in enumerate(_KEYS):
            for col, key in enumerate(keys):
                if key is None:
                    continue
                btn = QPushButton(key)
                btn.setFlat(True)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                buttons[key] = btn
                grid.addWidget(btn, row, col)
                if key == "=":
                    equals_btn = btn

        assert equals_btn is not None
        equals_btn.setObjectName("btnEquals")
        grid.addWidget(equals_btn, 3, 3, 2, 1)  # fusion verticale de "="

        for key, btn in buttons.items():
            btn.clicked.connect(lambda _checked=False, k=key: self._on_key(k))

        root.addWidget(pad)
        self.setCentralWidget(central)

    # ------------------------------------------------------------- actions

    def _on_key(self, key: str) -> None:
        if self._error and key != "C":
            self._on_clear()
        if key == "C":
            self._on_clear()
        elif key == "⌫":
            self._on_backspace()
        elif key == "=":
            self._on_equals()
        elif key in _OPERATOR_SYMBOLS:
            self._on_operator(operation_from_symbol(key))
        else:  # chiffre ou point
            self._on_digit(key)
        self._refresh_display()

    def _on_digit(self, key: str) -> None:
        if self._fresh_entry:
            self._current = "0." if key == "." else key
            self._fresh_entry = False
            return
        if self._current == "0" and key != ".":
            self._current = key
        elif key == "." and "." in self._current:
            return
        else:
            self._current += key

    def _on_operator(self, op: Operation) -> None:
        value = float(self._current)
        if self._acc is not None and self._pending_op is not None:
            # Chaînage d'opérations : évalue l'opération en attente
            try:
                self._acc = self._calc.compute(self._acc, self._pending_op, value)
            except ZeroDivisionError:
                self._show_error()
                return
        else:
            self._acc = value
        self._pending_op = op
        self._current = format_number(self._acc) if self._acc is not None else "0"
        self._fresh_entry = True

    def _on_equals(self) -> None:
        if self._acc is None or self._pending_op is None:
            return
        value = float(self._current)
        try:
            result = self._calc.compute(self._acc, self._pending_op, value)
        except ZeroDivisionError:
            self._show_error()
            return
        self._acc = None
        self._pending_op = None
        self._current = format_number(result)
        self._fresh_entry = True

    def _on_clear(self) -> None:
        self._acc = None
        self._pending_op = None
        self._current = "0"
        self._fresh_entry = True
        self._error = False
        self._calc.clear_history()

    def _on_backspace(self) -> None:
        self._current = self._current[:-1] or "0"

    def _show_error(self) -> None:
        self._error = True
        self._acc = None
        self._pending_op = None
        self._current = _ERROR_MESSAGE

    # ------------------------------------------------------------ affichage

    def _refresh_display(self) -> None:
        self._display.setText(self._current)

    # ------------------------------------------------------------- clavier

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 (API Qt)
        mapping: dict[Qt.Key, str] = {
            Qt.Key.Key_Return: "=",
            Qt.Key.Key_Enter: "=",
            Qt.Key.Key_Escape: "C",
            Qt.Key.Key_Backspace: "⌫",
            Qt.Key.Key_Slash: "÷",
            Qt.Key.Key_Asterisk: "×",
            Qt.Key.Key_Minus: "−",
            Qt.Key.Key_Plus: "+",
        }
        key: str | None = mapping.get(Qt.Key(event.key()))
        if key is None:
            text = event.text()
            if text in _DIGITS:
                key = text
        if key is not None:
            self._on_key(key)
        else:
            super().keyPressEvent(event)
