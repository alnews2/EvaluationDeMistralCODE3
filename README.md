# QuatreOps — Calculatrice à quatre opérations

Petite application de bureau (PySide6/Qt6) servant de **démonstration d'un socle
de développement logiciel de qualité** : architecture en couches, tests
automatisés, intégration continue multi-OS, livraison d'exécutables autonomes
Windows/Linux et documentation vivante.

## ✨ Fonctionnalités

- Les quatre opérations : addition, soustraction, multiplication, division
- Chaînage des opérations (`2 + 3 + 4 =`), affichage d'erreur sur division par zéro
- Saisie au clavier (chiffres, `+ - * /`, `Entrée` = `=`, `Échap` = `C`)
- Historique de session et effacement (touche `C`)

## 🚀 Démarrage rapide

### Depuis les sources

```bash
python -m venv .venv && source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -e .[dev]
quatre-ops            # ou : python -m calculator
```

### Exécutable autonome

Téléchargez le binaire de la dernière [release](../../releases) :
`quatre-ops-windows` (`.exe`) ou `quatre-ops-linux`.

## 🧪 Tests

```bash
pytest                 # tests complets + couverture (seuil 85 %)
pytest -k core         # moteur de calcul uniquement
```

Les tests d'IHM utilisent [pytest-qt](https://pytest-qt.readthedocs.io/) et
tournent sans écran (`QT_QPA_PLATFORM=offscreen`), donc en CI.

## 🛠️ Qualité

```bash
ruff check . && ruff format --check .   # lint + format
mypy                                    # typage strict
pre-commit run --all-files             # hooks git
```

## 📦 Construire un exécutable

```bash
pip install -e .[build]
pyinstaller --noconfirm --clean --onefile --windowed --name quatre-ops --paths src main.py
```

Un tag `v*.*.*` déclenche automatiquement la construction Windows + Linux et la
publication d'une [release GitHub](../../releases) avec les binaires joints.

## 📚 Documentation

- [Guide utilisateur](docs/user-guide.md)
- [Architecture technique](docs/architecture.md)
- [Guide de contribution](CONTRIBUTING.md)
- [Journal des versions](CHANGELOG.md)

## 🗺️ Feuille de route

- [ ] Touche `%` (pourcentage) et `±`
- [ ] Panneau d'historique visible dans l'IHM
- [ ] Paramètres de langue (fr/en) via Qt Linguist
- [ ] Raccourcis et thèmes clair/sombre

## 📄 Licence

MIT — voir [LICENSE](LICENSE).
