---
name: captures
description: Prendre les captures d'écran d'une validation : chaque page de pygabdev3 au téléphone et à l'ordinateur, le back-office avec le compte de démonstration connecté, une capture par point de la checklist. À utiliser à la fin d'une demande qui touche l'interface, ou quand Gabriel demande des captures.
---

# Captures d'une validation

Les captures montrent à Gabriel ce qu'il valide, sans qu'il lance le site.

## Avant

- Le site tourne (skill `lancer-app`), avec le compte de démonstration pour le back-office.
- Playwright pour Python, lancé par uv hors du dépôt : il n'entre pas dans `requirements.txt`. Son Chromium sans interface s'installe une fois (environ 200 Mo, dans `~/Library/Caches/ms-playwright`) :

```bash
uv run --no-project --with playwright==1.64.0 playwright install --only-shell chromium
```

## Prendre

À la racine du dépôt, une capture par page, nommée dans l'ordre de la checklist, chacune au téléphone (390 × 844, en 2x) et à l'ordinateur (1440 × 900) :

```bash
uv run --no-project --with playwright==1.64.0 python .claude/skills/captures/captures.py --out <dossier du scratchpad> 01-accueil=/ 02-blog=/blog/
uv run --no-project --with playwright==1.64.0 python .claude/skills/captures/captures.py --out <dossier du scratchpad> --device telephone "03-menu=/@Menu"
uv run --no-project --with playwright==1.64.0 python .claude/skills/captures/captures.py --out <dossier du scratchpad> --demo 04-projets=/customers/projects/
```

- `--device telephone` ou `--device ordinateur` ne prend qu'un gabarit : le bouton du menu n'existe qu'au téléphone, et un bouton caché fait échouer la capture.

- `--demo` connecte le compte de démonstration (skill `lancer-app`) par la connexion de l'admin Django, avec le mot de passe de `.env.example`. Sans lui, seules les pages publiques s'ouvrent.
- Un bouton à ouvrir avant la capture suit un « @ », par son nom accessible exact : le menu du téléphone (`Menu`), une modale. Plusieurs « @ » se suivent, dans l'ordre.
- Un « ~ » suivi d'un nombre attend autant de millisecondes, le temps d'une animation (`"03-menu=/@Menu~800"`).
- Le bandeau des cookies est refusé avant la première capture, et la barre de Wagtail est masquée.

## Montrer

- Regarder chaque capture avant de l'envoyer, et corriger ce qui cloche.
- Les envoyer à Gabriel par SendUserFile, dans l'ordre de la checklist, avec un mot par point.
