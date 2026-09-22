# Changelog

Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionnement [SemVer](https://semver.org/lang/fr/).

## [Non publié]

## [0.1.0] — 2026-09-22

### Ajouté

- Moteur de calcul (`calculator.core`) : les quatre opérations, historique de
  session, formatage des résultats, gestion de la division par zéro.
- Interface PySide6 : afficheur, pavé de touches, saisie clavier complète.
- Tests automatisés : unitaires (moteur) et d'IHM (pytest-qt, headless).
- CI GitHub Actions : lint (Ruff), typage (Mypy strict), tests sur matrice
  2 OS × 2 versions de Python, couverture ≥ 85 %.
- Livraison : workflow de release PyInstaller (`--onefile`) Windows + Linux,
  publication automatique d'une release GitHub sur tag `v*.*.*`.
- Documentation : README, guide utilisateur, architecture, contribution.
- Hooks pre-commit (lint, format, typage).
