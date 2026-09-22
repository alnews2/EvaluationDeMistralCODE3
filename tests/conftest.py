"""Configuration pytest : rend Qt utilisable sans écran (CI)."""

from __future__ import annotations

import os

# En environnement headless (CI Linux), forcer la plateforme offscreen AVANT
# l'import de Qt. Sur poste de travail, cette valeur est sans effet.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
