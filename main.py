"""Point d'entrée pour PyInstaller (le module de package pose des soucis de path)."""

from __future__ import annotations

from calculator.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
