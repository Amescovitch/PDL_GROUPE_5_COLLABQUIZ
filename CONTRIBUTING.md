# Guide de contribution

Merci de contribuer à CollabQuiz ! Ce guide décrit les attentes et règles pour contribuer (issues, branches, commits, PR).

## Avant de commencer
- Assure-toi d'avoir lu le `README.md` et de pouvoir lancer le projet en local (voir Quickstart).
- Ouvre une issue si tu veux demander une fonctionnalité ou signaler un bug avant de commencer à coder.

## Branching
- Travailler toujours à partir de la branche `main` ou d'une branche de fonctionnalité issue de `main`.
- Nommer les branches de fonctionnalité ainsi : `feat/<sujet>` ou `fix/<sujet>` (ex: `feat/auth-login`, `fix/session-ws`).

## Conventions de commit (Conventional Commits)
Nous utilisons les Conventional Commits pour garder un historique lisible et permettre des releases automatiques si besoin.

Format :

```
<type>(<scope>): <sujet>

<corps optionnel>

BREAKING CHANGE: <description>
```

Types courants :
- feat: ajout d'une fonctionnalité
- fix: correction d'un bug
- docs: modifications de la documentation
- style: formatage, lint, pas de changement fonctionnel
- refactor: refactoring sans ajout/correction de fonctionnalité
- perf: amélioration des performances
- test: ajout/modification de tests
- chore: tâches de maintenance (build, tooling)
- ci: changements CI/CD

Exemples :
- `feat(auth): add login route with JWT`
- `fix(api): handle null values in /quizzes response`
- `docs: update README Quickstart`
- `chore: bump backend dependencies`

Notes :
- Le `scope` est optionnel mais utile (ex: `backend`, `frontend`, `db`).
- Pour un changement cassant, indiquer `BREAKING CHANGE:` dans le corps du commit.

## Pull Requests
- Ouvrir une PR depuis ta branche de fonctionnalité vers `main`.
- Donner un titre clair et référencer l'issue associée (ex: `Closes #12`).
- Ajouter une description courte : objectif, changements majeurs, comment tester.
- Ajouter des reviewers (1 ou 2) et attendre au moins une approbation avant de merger.

## Tests & Lint
- Exécuter les tests backend : `pytest` (voir `backend/tests`).
- Exécuter les tests frontend : `npm run test` (vitest) si configuré.
- Respecter le style du projet. Nous recommandons d'ajouter ESLint / ruff plus tard pour automatiser.

## Style de code
- Backend : Python 3.11+, suivre PEP8 (utiliser `ruff`/`black` si possible).
- Frontend : Vue 3 + TypeScript partiel, suivre les conventions Vue + ESLint.

## Merci !
Merci pour ta contribution — n'hésite pas à demander de l'aide dans une issue ou un commentaire de PR.
