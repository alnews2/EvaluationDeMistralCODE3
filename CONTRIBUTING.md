# Contribuer à QuatreOps

Merci de votre intérêt ! Ce projet suit une discipline de développement
volontairement exigeante — c'est aussi un exercice de style.

## Boucle de développement

1. Créez une branche : `git switch -c feat/ma-fonctionnalite`
2. Codez dans `src/` (métier) et/ou `src/calculator/ui/` (IHM).
3. Ajoutez des tests dans `tests/` — toute nouvelle branche de logique doit
   être couverte.
4. Vérifiez localement :

   ```bash
   pre-commit run --all-files   # lint + format + types
   pytest                       # tests + couverture (seuil 85 %)
   ```

5. Ouvrez une **pull request** vers `main` : la CI rejoue toute la chaîne
   sur Linux et Windows.

## Conventions

- **Commits** : [Conventional Commits](https://www.conventionalcommits.org/fr/)
  (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `refactor:`…).
- **Versions** : SemVer. Toute release part d'un tag `v*.*.*` ; le CHANGELOG
  est mis à jour dans la même PR que la fonctionnalité.
- **Style** : Ruff est la référence (formatage + lint) ; pas de `# noqa`
  sans justification en commentaire.
- **Typage** : `mypy --strict` doit passer sans erreur ni stub manquant.
- **IHM** : aucune logique métier dans les widgets — tout passe par
  `calculator.core`.

## Signaler un bug

Ouvrez une [issue](../../issues) avec : étapes de reproduction, comportement
attendu/observé, système et version de l'application.

## Proposer une évolution

Les idées acceptées passent d'abord par une issue « proposition » discutée,
puis par une PR de taille raisonnable (petits pas incrémentaux > grosse PR).
