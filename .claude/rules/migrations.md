---
paths:
  - "**/models.py"
  - "**/migrations/*.py"
---

# Migrations

- Jamais écrite à la main : `./venv/bin/python manage.py makemigrations <app> --name <nom>`. Seule exception, une migration de données : `makemigrations <app> --empty --name <nom>`, complétée par un `RunPython` avec son `reverse_code`, et testée.
- Une migration poussée sur `main` ne se modifie jamais. Aucun hook ne la réécrit : ruff exclut les migrations (`ruff.toml`).
- Un changement des blocs d'un `StreamField` produit une migration, qui se commite (`.claude/rules/wagtail.md`).
- **SQLite en local et en tests, MySQL en prod** (`STRICT_TRANS_TABLES`) : ce que SQLite tolère peut échouer en prod, comme un texte plus long que son `max_length`. Pas de SQL brut : une migration de données passe par l'ORM (`apps.get_model`).
- **Sûre pour le déploiement** : il tire le code, migre la base, puis redémarre gunicorn. Entre les deux, l'ancien code tourne sur le schéma migré.
  - On ajoute d'abord, on retire dans un déploiement suivant.
  - Pas de renommage ni de suppression d'une colonne encore lue par le code en place.
  - Une colonne NOT NULL ajoutée porte un `db_default` en plus de son `default`.
- Une migration qui touche des données de prod (factures, prestations, contenus publiés) se signale à Gabriel avant le déploiement : il décide d'une sauvegarde de la base.
