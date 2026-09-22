# Architecture technique

## Vue d'ensemble

```
┌────────────────────────────────────────────┐
│                 IHM (PySide6)              │
│         src/calculator/ui/main_window.py   │
│      traduit clics/clavier → commandes     │
└──────────────────┬─────────────────────────┘
                   │ appelle
┌──────────────────▼─────────────────────────┐
│              Logique métier                │
│        src/calculator/core.py              │
│  Calculator, Operation, evaluate, format   │
│         (pur Python, zéro dépendance)      │
└────────────────────────────────────────────┘
```

## Principes

1. **Séparation stricte des responsabilités** — `core.py` est du Python pur
   sans import Qt. Il est testable en une milliseconde, réutilisable (CLI,
   web…), et l'IHM n'est qu'une « coquille » fine.
2. **Layout `src/`** — évite l'import accidentel du paquet depuis le répertoire
   courant ; les tests exercent la version *installée*.
3. **Typage strict** — `mypy --strict` sur `src/` ; le code est pensé pour
   être sûr dès l'écriture, pas corrigé après coup.
4. **Comportement explicite** — la division par zéro lève `ZeroDivisionError`
   côté moteur et devient un message « Erreur » récupérable côté IHM ; une
   entrée d'historique n'est jamais écrite si le calcul échoue.

## Format des nombres

Le moteur travaille en flottants IEEE-754 (`float`). L'affichage arrondit à
10 chiffres significatifs (`0.1 + 0.2` s'affiche `0.3`). Un passage en
`decimal.Decimal` est une évolution possible si la précision exacte devient
un besoin.

## Chaîne de qualification

| Étape            | Outil          | Déclencheur                |
|------------------|----------------|----------------------------|
| Lint & format    | Ruff           | pre-commit + CI            |
| Typage           | Mypy (strict)  | pre-commit + CI           |
| Tests            | pytest + pytest-qt, matrice OS × Python | CI |
| Couverture       | pytest-cov, seuil 85 % | CI             |
| Packaging        | PyInstaller `--onefile` | tag `v*`      |

## Points d'extension prévus

- **Nouvelle opération** : ajouter un membre à `Operation`, une branche à
  `evaluate`, un symbole au pavé. Aucune refonte.
- **Historique visible** : `Calculator.history` existe déjà côté métier ;
  il reste à l'afficher (QListWidget).
- **i18n** : remplacer les chaînes brutes par `QCoreApplication.translate()`
  et générer les `.qm` via Qt Linguist.
- **Moteur alternatif** : `core.py` n'ayant aucune dépendance, une implémentation
  à précision arbitraire peut le remplacer sans toucher l'IHM (à condition de
  conserver l'API `compute/evaluate`).
