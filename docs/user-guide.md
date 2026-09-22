# Guide utilisateur

## Lancer l'application

- **Depuis les sources** : `quatre-ops` (après `pip install -e .`)
- **Binaire autonome** : double-cliquez sur `quatre-ops.exe` (Windows) ou
  lancez `./quatre-ops-linux` (Linux).

## Utilisation

| Action                   | Souris        | Clavier              |
|--------------------------|---------------|----------------------|
| Saisir un nombre         | `0–9`, `.`    | `0–9`, `.`           |
| Addition / soustraction  | `+` / `−`     | `+` / `-`            |
| Multiplication / division| `×` / `÷`     | `*` / `/`            |
| Calculer                 | `=`           | `Entrée`             |
| Effacer tout             | `C`           | `Échap`              |
| Corriger le dernier chiffre | `⌫`        | `Retour arrière`     |

### Exemples

- `2 + 3 + 4 =` → **9** (chaînage : le second `+` évalue déjà `2 + 3`)
- `10 ÷ 4 =` → **2.5**
- `5 ÷ 0 =` → **Erreur** ; appuyez sur `C` (ou toute touche) pour repartir de zéro

## Points à connaître

- Les nombres trop longs pour l'afficheur sont tronqués visuellement mais
  conservés en mémoire.
- Les résultats sont arrondis à 10 chiffres significatifs.
- L'historique de session est effacé par `C` ou à la fermeture de l'application.

## Signaler un problème

Ouvrez une [issue](../../issues) en décrivant : le système, la version,
les touches pressées et le résultat attendu.
