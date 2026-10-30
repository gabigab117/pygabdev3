
# Mon Application Personnelle

Bienvenue sur mon application personnelle, conçue avec **Django Wagtail**, pour montrer mes articles de blog sur Python, Django et Wagtail, présenter mes projets, et gérer en backoffice mes clients et projets.

## Fonctionnalités Principales

- **Portfolio** : Une présentation de mes projets et articles pour partager mon travail et mes idées.
- **Blog** : J'adore partager à propos de Python, Django et Wagtail.
- **Back-office** : Gestion des clients, projets et services, avec le suivi de ce qui reste à facturer. Les factures se font sur facture.net ; les anciennes restent consultables, en lecture seule, dans l'admin Django.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/gabigab117/pygabdev3.git
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Appliquez les migrations de base de données :
   ```bash
   python manage.py migrate
   ```

4. Lancez le serveur de développement :
   ```bash
   python manage.py runserver
   ```

## Technologies

- **CMS** : Wagtail (pour la gestion de contenu).
- **Backend** : Django.
- **Frontend** : Tailwind CSS pour un design moderne et épuré.
- **HTMX** : Recherche dynamique avec HTMX
- **Base de données** : SQLite (en développement, configurable).
- Ici j'ai laissé les fichiers Docker, mais ils ne sont pas utilisés (pour le moment).
