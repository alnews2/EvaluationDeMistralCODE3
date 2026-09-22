"""Tests d'intégration de l'interface graphique (pytest-qt)."""

from __future__ import annotations

import pytest

from calculator.ui.main_window import MainWindow


@pytest.fixture()
def window(qtbot) -> MainWindow:
    win = MainWindow()
    qtbot.addWidget(win)
    return win


def _press(window: MainWindow, *keys: str) -> None:
    for key in keys:
        window._on_key(key)  # noqa: SLF001 — test blanc, accès contrôlé


def test_addition_simple(window: MainWindow) -> None:
    _press(window, "1", "+", "2", "=")
    assert window._display.text() == "3"  # noqa: SLF001


def test_soustraction_resultat_negatif(window: MainWindow) -> None:
    _press(window, "5", "−", "7", "=")
    assert window._display.text() == "-2"  # noqa: SLF001


def test_multiplication_et_division(window: MainWindow) -> None:
    _press(window, "3", "×", "4", "=")
    assert window._display.text() == "12"  # noqa: SLF001
    _press(window, "C")
    _press(window, "1", "0", "÷", "4", "=")
    assert window._display.text() == "2.5"  # noqa: SLF001


def test_division_par_zero_affiche_erreur(window: MainWindow) -> None:
    _press(window, "5", "÷", "0", "=")
    assert window._display.text() == "Erreur"  # noqa: SLF001
    # Un appui sur une touche remet à zéro
    _press(window, "7")
    assert window._display.text() == "7"  # noqa: SLF001


def test_chainage_d_operations(window: MainWindow) -> None:
    """2 + 3 + 4 = : le '+' intermédiaire doit évaluer 2+3."""
    _press(window, "2", "+", "3", "+", "4", "=")
    assert window._display.text() == "9"  # noqa: SLF001


def test_entree_fraiche_apres_operateur(window: MainWindow) -> None:
    """Après '+', la saisie doit recommencer à zéro (pas '12+34')."""
    _press(window, "1", "2", "+", "3", "4", "=")
    assert window._display.text() == "46"  # noqa: SLF001


def test_clear_et_backspace(window: MainWindow) -> None:
    _press(window, "1", "2", "3")
    assert window._display.text() == "123"  # noqa: SLF001
    _press(window, "⌫")
    assert window._display.text() == "12"  # noqa: SLF001
    _press(window, "C")
    assert window._display.text() == "0"  # noqa: SLF001


def test_point_decimal_unique(window: MainWindow) -> None:
    _press(window, "1", ".", "5", ".", "5")
    assert window._display.text() == "1.55"  # noqa: SLF001


def test_equals_sans_operateur_ne_fait_rien(window: MainWindow) -> None:
    _press(window, "4", "=")
    assert window._display.text() == "4"  # noqa: SLF001
