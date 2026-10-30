---
name: lancer-app
description: Démarrer pygabdev3 en local (base SQLite, compte de démonstration, runserver) pour l'essayer, le parcourir dans le navigateur intégré ou en prendre des captures. À utiliser avant toute vérification dans le site, avant la skill `captures`, ou quand Gabriel demande de lancer le site.
---

# Lancer pygabdev3 en local

Une commande qui change s'écrit ici, jamais en mémoire. Toutes se lancent à la racine du dépôt.

## 1. La base

- SQLite, dans `db.sqlite3` (ignoré par git) : la base de travail de Gabriel, avec ses pages Wagtail. Elle ne se supprime ni ne se remplace jamais.
- Après un `git pull` qui apporte des migrations : `./venv/bin/python manage.py migrate`.
- Sur un clone neuf : `cp .env.example .env`, puis Gabriel y met ses valeurs ; `migrate`, et le site n'a encore aucune page : elles se créent dans l'admin Wagtail.

## 2. Le compte de démonstration

Un superuser fictif, `demo`, pour le back-office et les admins. Son mot de passe est pris dans `.env.example` et passé sur la ligne de commande : le `.env` de Gabriel n'a pas à changer. Jamais sur le serveur.

```bash
DJANGO_SUPERUSER_PASSWORD="$(sed -n 's/^DEMO_PASSWORD=//p' .env.example)" ./venv/bin/python manage.py createsuperuser --noinput --username demo --email demo@example.org
```

S'il existe déjà, la commande répond que le nom est pris : rien à faire.

## 3. Le serveur

Claude le lance en arrière-plan (`run_in_background`) ; Gabriel, dans un terminal.

```bash
./venv/bin/python manage.py runserver 127.0.0.1:8000
```

Prêt quand le site répond, sans `sleep` :

```bash
curl -s -o /dev/null -w '%{http_code}\n' --retry 30 --retry-delay 1 --retry-connrefused http://localhost:8000/
```

La réponse attendue : `200`.

- Les pages publiques ont l'adresse de leur slug dans la base locale : `/`, `/blog/`, `/projets/`, `/contact/`, `/legal/`.
- Le back-office est sous `/customers/` (le tableau de bord : `/customers/dashboard/`). Sans session, il renvoie à la connexion de l'admin Django : on suit ce renvoi.
- Les adresses des admins sont dans le `.env` de Gabriel (`DJANGO_ADMIN_URL`, `WAGTAIL_ADMIN_URL`), que Claude ne lit pas.

## 4. Les e-mails

`base.py` règle le SMTP de Gmail pour tous les settings : en local, un message du formulaire de contact part vraiment, avec les identifiants du `.env`. Ce formulaire ne se soumet pas sans l'accord de Gabriel.

## 5. Sur le vrai téléphone

Le Mac et le téléphone sur le même wifi :

```bash
ALLOWED_HOSTS="localhost,127.0.0.1,<adresse du Mac>" ./venv/bin/python manage.py runserver 0.0.0.0:8000
```

Puis `http://<adresse du Mac>:8000` sur le téléphone. Une variable passée sur la ligne de commande l'emporte sur le `.env` (django-environ ne l'écrase pas).

## Arrêter

Claude arrête sa tâche de fond (TaskStop). Gabriel fait Ctrl+C.
