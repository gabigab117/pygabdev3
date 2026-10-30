# pygabdev3 : règles du projet

pygab.dev, le site de Gabriel, développeur freelance. Un site public en Wagtail (accueil, réalisations, blog, contact, pages légales), qui doit convaincre des prospects, et un back-office Django privé (clients, projets, prestations ; les anciennes factures en archive). Les règles propres à un type de fichier vivent dans `.claude/rules/` et se chargent quand on touche ces fichiers.

**Le dépôt est public sur GitHub.** Rien de privé n'entre dans le code, ce fichier ou `.claude/` : ni secret, ni adresse, utilisateur ou chemin du serveur. Ce qui décrit la prod reste dans la skill locale `deployer`, ignorée par git.

## Structure

```
pygabdev3/
├── project/     settings (base, dev, production), urls, gabarits communs (base.html, includes/)
├── core/        GenericPage (abstraite : l'en-tête) et LegalPage
├── home/ blog/ folio/ tag/ contact/ search/   les pages Wagtail du site public
├── customers/   le back-office, réservé au staff
├── account/     CustomUser (AUTH_USER_MODEL)
├── static/      css/styles.css (la couche de thème de Bootstrap), js/script.js, logos/
├── tests/       pytest : conftest.py, factories.py
└── .claude/     réglages, hook git, règles par chemin, skills
```

## Sources de vérité

- **Le périmètre, c'est la demande de Gabriel** : ce qu'elle ne dit pas ne se code pas. Une question ouverte se pose avant le code, pas après.
- **Une contradiction se signale, elle ne se tranche jamais en silence** : entre le code, ce fichier, le README ou une demande.
- Le contenu publié (articles, réalisations, pages légales) vit dans la base de prod, saisi dans l'admin Wagtail. Les textes de vente de l'accueil sont dans son gabarit.

## Workflow

- **Une demande à la fois**, puis arrêt et compte rendu. Avant : lire les fichiers qu'elle touche, puis interroger Context7 sur les librairies concernées. Une demande non triviale commence par un plan (étapes, fichiers, tests), validé avant le code.
- **Le passage de la doc au code s'annonce** en une ligne (« je passe au code : …, pas encore … »), même quand le plan validé le prévoyait.
- **Clôture d'une demande**, dans cet ordre :
  1. code et tests verts ;
  2. passe de simplification (section plus bas) ;
  3. contrôles relancés (Definition of Done) ;
  4. commit puis push ;
  5. CI verte.
- **Le déploiement ne fait pas partie de la clôture** : il se fait seulement quand Gabriel le demande (skill `deployer`). Un push sur `main` ne déploie rien.
- **Une validation se demande par une checklist courte et numérotée**, séparée du compte rendu : quoi regarder, quoi décider. Elle finit par « Un OK suffit, ou dis ce qu'il faut changer ».
- Conventional commits en anglais, directement sur `main`, historique linéaire (rebase seulement). Push sans redemander : le distant sert de sauvegarde. Une branche et une PR seulement quand Gabriel les demande.

## Garde-fous

Tout ce qu'une machine peut vérifier l'est (hook, pre-commit, CI, test) ; ce fichier ne dit que pourquoi.

- **Le hook `.claude/hooks/garde_git.py` refuse** `git checkout`, `git restore` sur les fichiers de travail, `git reset --hard`, `git clean -f`, `git switch -f`, `git stash drop` ou `clear`, et tout force-push, même lancés par `git -C`. Ces commandes effacent un travail non commité, et c'est déjà arrivé sur un autre projet. Pour changer de branche : `git switch`.
- **Une mutation volontaire** (prouver qu'un test attrape un défaut) se fait sur une copie : copier le fichier dans le scratchpad, muter, restaurer depuis la copie, puis vérifier `git diff --stat`.
- **La lecture des `.env` est refusée** (`permissions.deny`), par Read comme par `cat` : un secret lu finit dans la conversation. Le modèle à lire est `.env.example`. La règle s'écrit `Read(~/**/.env)` : sans `~/` ni `/` en tête, elle se compterait depuis le dossier courant.
- **En local, aucun e-mail ne part** : `dev.py` les affiche dans la console de `runserver`, à la place du SMTP de Gmail que `base.py` garde pour la prod. Un test le vérifie (`tests/test_settings.py`). Les tests, eux, passent par la boîte en mémoire de Django.
- Le pre-commit refuse un CLAUDE.md ou une règle de `.claude/rules/` de plus de 150 lignes : selon la documentation de Claude Code, un fichier long est moins bien suivi.

## Documentation à jour (Context7, obligatoire)

- Avant d'écrire ou de modifier du code qui s'appuie sur une librairie : Context7, puis la documentation officielle, puis le code installé (`venv/`). Toujours pour la version de `requirements.txt`, jamais de mémoire.
- Le piège de cette stack : beaucoup d'exemples en ligne visent Wagtail 2 à 5 (`wagtail.core`, `edit_handlers`), Bootstrap 4 (`data-toggle` au lieu de `data-bs-toggle`) ou HTMX 1. Ici : Django 5.2, Wagtail 7.4, Bootstrap 5.3, HTMX 2.

## Ne rien réinventer

- **Déclencheur** : on s'apprête à écrire du code qui *ressemble* à une fonctionnalité de framework (validation, unicité, filtrage, pagination, permissions, recherche, formulaires, images, dates). On cherche alors le natif de Django ou de Wagtail dans Context7, **avant** d'écrire, pas après.
- Si le natif est écarté, un commentaire dit pourquoi, à côté du code.
- Une librairie entre dès qu'elle simplifie le code, et seulement alors : cherchée dans Context7 comme le natif, épinglée dans `requirements.txt`.
- YAGNI : pas de code pour une demande qui n'est pas faite. Pas de code mort ; les commentaires disent pourquoi, pas quoi.

## Conventions

- **Code en anglais, interface en français.**
  - En anglais : modèles, champs, variables, fichiers, adresses du back-office, commentaires, docstrings, commits.
  - En français : textes du site, `verbose_name`, `help_text`, libellés, messages d'erreur, documents du projet.
- **Glossaire** : `.claude/rules/glossaire.md`, chargé dès qu'on touche au code. Un mot nouveau y entre avant d'être utilisé ; un nom qui s'en écarte est un défaut.
- **Aucun quadratin (—) dans un texte rédigé** (page du site, commit, commentaire, compte rendu) : Gabriel le trouve typique de l'IA, et un site qui sonne IA dessert un développeur freelance. Une virgule, un deux-points ou une parenthèse à la place.
- Secrets par les variables d'environnement (`django-environ`), jamais dans le code. Données de test et de démonstration fictives, toujours.

## Architecture

- **Site public** : des pages Wagtail (`.claude/rules/wagtail.md`). **Back-office** : des vues génériques de Django dans `customers/`, derrière `staff_member_required` (`.claude/rules/back-office.md`).
- **Gabarits Django, sans build front** : Bootstrap 5.3 par CDN, la couche de thème `static/css/styles.css`, HTMX pour la recherche du back-office (`.claude/rules/gabarits.md`).
- Settings : `base`, `dev` (DEBUG, SQLite), `production` (MySQL, HTTPS, HSTS, `ManifestStaticFilesStorage`, journal dans `logs/`). `manage.py` lit `DJANGO_SETTINGS_MODULE` dans le `.env`, `dev` par défaut.
- Les adresses des deux admins viennent de l'environnement (`DJANGO_ADMIN_URL`, `WAGTAIL_ADMIN_URL`) et restent hors du dépôt : un gabarit ou un test les obtient par `{% url %}` ou `reverse()`, jamais écrites en dur.
- Cookies par django-cookie-consent : Google Tag Manager ne se charge qu'après accord ; Simple Analytics, sans cookie, hors back-office.

## Commandes

- `./venv/bin/pip install -r requirements.txt` : pip et le venv du dépôt. `requirements.txt` épingle chaque paquet, outils de test compris ; une mise à jour le modifie à la main.
- `./venv/bin/pytest` : les tests.
- `pre-commit run --all-files` (pre-commit vient de Homebrew ; `pre-commit install` une fois par clone) : ruff (lint et format), gitleaks, `makemigrations --check`, longueur des CLAUDE.md et des règles, tests du hook git. La CI rejoue les mêmes hooks, puis pytest.
- `./venv/bin/python manage.py makemigrations <app> --name <nom>` (règles : `.claude/rules/migrations.md`).
- Lancer le site en local : skill `lancer-app`. Les captures d'une validation : skill `captures`. Le déploiement : skill `deployer`, locale, sur demande seulement.

## Tests (pytest)

- Tests en fonctions, jamais en classes, dans `tests/`. Fixtures dans `tests/conftest.py`, objets par factory_boy (`tests/factories.py`). Un fichier envoyé passe par la fixture `media_root`.
- Chaque test nouveau a une docstring en Gherkin, en anglais, comme ceux de `tests/test_views.py` :

  ```python
  def test_projects_view_filtered_by_customer(client, admin, project_1, project_3, customer_1):
      """
      Scenario: Filter the projects list by customer
          Given I am an authenticated administrator
              And projects exist for several customers
          When I request the projects list filtered on one customer
          Then only that customer's projects are returned
      """
  ```
- Requêtes par le `client` de Django, connecté par `force_login`.
- Les cas d'erreur comptent autant que les cas nominaux : un anonyme et un compte non staff renvoyés à la connexion, un formulaire invalide, un objet inconnu (404).
- Pas de seuil de couverture : toute logique nouvelle arrive avec ses tests, et un défaut avec le test qui le prouve, écrit d'abord.

## Passe de simplification

La skill `passe-simplification` lit cette section.

- **Quand** : à la fin de chaque demande et de chaque correctif, sur leur diff. Pas pour des docs seules, des tests seuls ou une ligne. Une petite demande, sans logique nouvelle, se relit sans agent.
- **Ordre de clôture** : celui du workflow. Un défaut relevé part dans son propre commit `fix:`, son test écrit d'abord.
- **Pièces partagées à comparer** : `core/models.py` (`GenericPage`, `LegalPage`), `project/templates/base.html` et `includes/` (navbar, footer), `customers/templates/customers/_pager.html`, `customers/forms.py`, les vues génériques de `customers/views.py`, les tokens et composants de `static/css/styles.css`, `static/js/script.js`, `tests/conftest.py`, `tests/factories.py`. Chaque demande qui crée une pièce partagée l'ajoute ici.
- **Règles maison** :
  - comportement identique : aucun texte, style, adresse ni migration ne bouge. Un constat qui toucherait l'un d'eux revient à Gabriel ;
  - un nom qui s'écarte du glossaire est un constat ;
  - remplacer du code par du natif passe d'abord par Context7.
- **Contrôles à relancer** : `./venv/bin/pytest` et `pre-commit run --all-files`.
- **Vu hors du diff** : noté dans le compte rendu à Gabriel, jamais dans le commit de la demande.

## Definition of Done

1. Context7 consulté pour chaque API de librairie utilisée ou modifiée.
2. `pre-commit run --all-files` passe.
3. `./venv/bin/pytest` est vert, avec des tests en Gherkin pour toute logique nouvelle, cas d'erreur et permissions compris.
4. Migrations générées par `makemigrations` et sûres pour le déploiement (`.claude/rules/migrations.md`).
5. Aucun code maison qui double une fonctionnalité native sans un commentaire qui dit pourquoi.
6. Écran validé sur captures par Gabriel, au téléphone et à l'ordinateur, quand la demande en touche un.
7. Commit poussé, CI verte.
