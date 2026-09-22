"""Tests unitaires du moteur de calcul (sans Qt)."""

from __future__ import annotations

import math

import pytest

from calculator.core import (
    Calculator,
    HistoryEntry,
    Operation,
    evaluate,
    format_number,
    operation_from_symbol,
)


@pytest.mark.parametrize(
    ("a", "op", "b", "expected"),
    [
        (2, Operation.ADD, 3, 5),
        (2.5, Operation.ADD, 0.5, 3.0),
        (10, Operation.SUBTRACT, 4, 6),
        (5, Operation.SUBTRACT, 7, -2),
        (3, Operation.MULTIPLY, 4, 12),
        (2.5, Operation.MULTIPLY, 4, 10.0),
        (10, Operation.DIVIDE, 4, 2.5),
        (7, Operation.DIVIDE, 2, 3.5),
        (-8, Operation.DIVIDE, 2, -4),
    ],
)
def test_evaluate(a: float, op: Operation, b: float, expected: float) -> None:
    assert evaluate(a, op, b) == pytest.approx(expected)


def test_division_par_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        evaluate(1, Operation.DIVIDE, 0)


def test_format_nombres() -> None:
    assert format_number(6.0) == "6"
    assert format_number(-4.0) == "-4"
    assert format_number(2.5) == "2.5"
    # Artefact binaire masqué par l'arrondi à 10 chiffres significatifs
    assert format_number(0.1 + 0.2) == "0.3"
    assert format_number(1 / 3) == "0.3333333333"


def test_historique() -> None:
    calc = Calculator()
    calc.compute(2, Operation.ADD, 3)
    calc.compute(10, Operation.DIVIDE, 4)

    assert len(calc.history) == 2
    assert calc.history[0].result == 5
    assert calc.history[0].as_text() == "2 + 3 = 5"
    assert calc.history[1].as_text() == "10 ÷ 4 = 2.5"

    calc.clear_history()
    assert calc.history == []


def test_symboles_operations() -> None:
    assert operation_from_symbol("×") is Operation.MULTIPLY
    assert operation_from_symbol("÷") is Operation.DIVIDE
    with pytest.raises(KeyError):
        operation_from_symbol("?")


def test_entree_historique_immuable_sur_erreurs() -> None:
    """Une division par zéro ne doit pas polluer l'historique."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.compute(1, Operation.DIVIDE, 0)
    assert calc.history == []


def test_precision_flottante() -> None:
    """Le moteur utilise les flottants IEEE-754 : documenter le comportement."""
    assert evaluate(0.1, Operation.ADD, 0.2) == pytest.approx(0.3)
    assert math.isfinite(evaluate(1e308, Operation.MULTIPLY, 10)) is False  # inf


def test_dataclass_historique() -> None:
    entry = HistoryEntry(left=2, op=Operation.ADD, right=3, result=5)
    assert (entry.left, entry.right, entry.result) == (2, 3, 5)
