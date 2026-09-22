"""Point d'entrée console (``quatre-ops`` ou ``python -m calculator``)."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from calculator import __version__
from calculator.ui.main_window import MainWindow


def main(argv: list[str] | None = None) -> int:
    """Lance l'application et retourne le code de sortie Qt."""
    app = QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName("QuatreOps")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("QuatreOps")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
