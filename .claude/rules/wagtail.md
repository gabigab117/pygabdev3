---
paths:
  - "home/**"
  - "blog/**"
  - "folio/**"
  - "core/**"
  - "tag/**"
  - "contact/**"
  - "search/**"
---

# Pages Wagtail

Le site public est fait de pages Wagtail, dont le contenu vit dans la base de prod, saisi par Gabriel dans l'admin. Un changement de modèle doit garder lisible tout ce qui est déjà publié.

- Une page hérite de `core.models.GenericPage` (son `header`), et ses `content_panels` partent de ceux de `GenericPage`. Panneaux, libellés et `help_text` en français.
- Une page index déclare ses `subpage_types` : l'admin ne propose alors que les pages qui ont leur gabarit sous elle.
- **Un `StreamField` est un document JSON stocké.** Le nom d'un bloc (`paragraphe`, `code`) est la clé des contenus publiés : le renommer ou le retirer les rend illisibles. On ajoute le nouveau bloc, une migration de données convertit les contenus, testée, et l'ancien bloc part dans un commit suivant.
- **Lectures dans `get_context`** :
  - `.live()` toujours, `.child_of(self)` pour les enfants d'un index ;
  - `.specific()` quand on lit les champs d'un type de page depuis `Page` ;
  - `prefetch_related` sur une relation lue dans la boucle (les dépôts d'une réalisation) ;
  - les images d'une liste par `Prefetch("main_image", queryset=Image.objects.prefetch_renditions("fill-720x450"))`, plutôt qu'une requête par carte.
- **Recherche** : le backend `database` de Wagtail. Un champ texte qui doit être trouvé entre dans `search_fields` ; `search/views.py` cherche dans `Page.objects.live()`.
- **Images** : `{% image %}` avec un filtre de rendition (`fill-720x450`), jamais l'URL du fichier d'origine, et toujours un `alt`.
- **Liens entre pages** : `{% pageurl %}` ou `{% slugurl %}`, jamais une adresse écrite en dur. `{% slugurl %}` dépend du slug saisi dans l'admin (`projets`, `contact`) : un slug changé casse le lien sans erreur.
- **Formulaire de contact** : `contact.FormPage` hérite de `WagtailCaptchaEmailForm` (reCAPTCHA) ; ses champs se déclarent dans l'admin. Un envoi part par e-mail, en local aussi (garde-fou du CLAUDE.md).
- Les textes de vente de l'accueil sont dans `home/templates/home/home_page.html`, avec `page.header` en priorité ; les articles, réalisations et pages légales dans l'admin. Un texte ne se duplique pas entre les deux.
- Un lien vers l'admin Wagtail passe par `{% url 'wagtailadmin_home' %}` : son adresse vient de `WAGTAIL_ADMIN_URL`.
