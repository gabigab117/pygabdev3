---
paths:
  - "**/templates/**/*.html"
  - "static/css/**"
  - "static/js/**"
---

# Gabarits et styles

Le site sert à convaincre des prospects : un texte maladroit ou un écran cassé au téléphone coûte un client.

- Un gabarit étend `project/templates/base.html` et remplit ses blocs (`banner`, `banner_title`, `banner_text`, `content`, `main_class`). Navbar et footer vivent dans `project/templates/includes/`.
- **Bootstrap 5.3 d'abord** (CDN, dans `base.html`) : grille, utilitaires, composants, attributs `data-bs-*`. Avant d'écrire un composant, on cherche le sien dans Bootstrap (Context7).
- **Puis la couche de thème** `static/css/styles.css`, chargée après Bootstrap :
  - ses tokens vivent dans `:root` (`--accent`, `--ink`, `--surface`, `--border`, `--r-md`, `--sh-md`…), et elle thème Bootstrap par ses variables `--bs-*` ;
  - une classe maison ne recouvre pas un nom de Bootstrap ;
  - aucune couleur, taille ou ombre écrite en dur, et pas d'attribut `style` nouveau : une valeur qui revient devient un token. Les styles nouveaux vont dans `styles.css`.
- Polices : Hanken Grotesk pour le texte, JetBrains Mono pour les titres et les étiquettes, par Google Fonts. Icônes : Bootstrap Icons.
- **JavaScript** : `static/js/script.js`, sans framework ni build. HTMX 2 pour la recherche du back-office. Une librairie chargée par CDN porte une version épinglée et son `integrity`.
- Pas de logique dans un gabarit au-delà d'un `if` ou d'un `for` : un calcul va dans `get_context` ou dans la vue.
- **Textes en français, pour des prospects** : clairs, concrets, au vouvoiement, sans jargon inutile. Aucun quadratin (—). Un texte nouveau du site se relit avec la skill `humanizer` avant d'être proposé à Gabriel.
- **Cookies et mesure d'audience** : Google Tag Manager ne se charge que si le groupe `analytics` est accepté (`cookie_group_accepted`) ; Simple Analytics, sans cookie, reste hors du back-office et des aperçus. Tout traceur nouveau passe par django-cookie-consent.
- **Référencement** : `seo_title`, `search_description` et lien canonique viennent de `base.html`. Un seul `h1` par page, un `alt` sur toute image.
- **Lisible par tous** : contrastes AA, focus visible, libellé sur toute icône seule (`aria-label` ou `visually-hidden`).
- **Deux gabarits** : le téléphone (390 px) et l'ordinateur (1440 px). Un écran nouveau ou retouché se dessine avec la skill `frontend-design`, puis se valide sur captures, aux deux tailles (skill `captures`).
