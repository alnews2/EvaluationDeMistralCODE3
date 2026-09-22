"""Moteur de calcul pur, sans aucune dépendance à Qt.

Ce module isole toute la logique métier afin qu'elle soit testable
indépendamment de l'interface graphique.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Operation(Enum):
    """Les quatre opérations supportées."""

    ADD = "+"
    SUBTRACT = "−"
    MULTIPLY = "×"
    DIVIDE = "÷"


_SYMBOLS: dict[str, Operation] = {op.value: op for op in Operation}


def operation_from_symbol(symbol: str) -> Operation:
    """Retourne l'opération correspondant à son symbole d'affichage.

    Raises:
        KeyError: si le symbole est inconnu.
    """
    return _SYMBOLS[symbol]


def evaluate(a: float, op: Operation, b: float) -> float:
    """Applique l'opération ``op`` aux opérandes ``a`` et ``b``.

    Raises:
        ZeroDivisionError: en cas de division par zéro.
    """
    if op is Operation.ADD:
        return a + b
    if op is Operation.SUBTRACT:
        return a - b
    if op is Operation.MULTIPLY:
        return a * b
    if op is Operation.DIVIDE:
        if b == 0:
            raise ZeroDivisionError("Division par zéro")
        return a / b
    raise ValueError(f"Opération non supportée : {op!r}")  # pragma: no cover


def format_number(value: float) -> str:
    """Formate un résultat numérique pour l'affichage.

    Les entiers sont affichés sans décimale ; les flottants sont
    arrondis à 10 chiffres significatifs pour masquer les artefacts binaires.
    """
    if value == int(value):
        return str(int(value))
    return f"{value:.10g}"


@dataclass
class HistoryEntry:
    """Une entrée d'historique de calcul."""

    left: float
    op: Operation
    right: float
    result: float

    def as_text(self) -> str:
        """Représentation textuelle, ex. ``2 × 3 = 6``."""
        return (
            f"{format_number(self.left)} {self.op.value} "
            f"{format_number(self.right)} = {format_number(self.result)}"
        )


@dataclass
class Calculator:
    """Calculatrice à état : conserve l'historique des calculs effectués."""

    history: list[HistoryEntry] = field(default_factory=list)

    def compute(self, a: float, op: Operation, b: float) -> float:
        """Évalue ``a op b``, enregistre l'entrée et retourne le résultat."""
        result = evaluate(a, op, b)
        self.history.append(HistoryEntry(a, op, b, result))
        return result

    def clear_history(self) -> None:
        """Vide l'historique."""
        self.history.clear()
