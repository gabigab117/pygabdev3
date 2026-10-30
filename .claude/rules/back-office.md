---
paths:
  - "customers/**"
  - "tests/**"
---

# Back-office

Le back-office (`customers/`) ne sert qu'à Gabriel : clients, projets, prestations. Les totaux et l'état « facturé » se prouvent par des tests.

**Les factures se font sur facture.net** depuis octobre 2026. Celles d'avant restent en base et leurs PDF dans `media/factures/` : l'admin Django les montre en lecture seule (`InvoiceAdmin`), et aucune page du back-office ne crée plus de facture. Rien n'efface cette archive, ni la table ni les fichiers.

- **Privé** : toute vue porte `staff_member_required`, en décorateur sur une fonction, par `method_decorator(staff_member_required, name="dispatch")` sur une classe. Un anonyme et un compte non staff sont renvoyés à la connexion de l'admin Django (302). Une vue nouvelle a ce test.
- **Vues génériques de Django** (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`), pagination par `paginate_by` et le gabarit `_pager.html`. Une liste lit ses relations par `select_related` (`ProjectList` le fait).
- **Les invariants de la facturation**, tenus par les modèles et leurs signaux (`customers/models.py`) :
  - le total d'une prestation vaut son `time_spent` multiplié par le `hourly_rate` de son projet, calculé à l'enregistrement (`Service.save`) ;
  - une prestation rattachée à une facture est `billed`, détachée elle ne l'est plus (`m2m_changed`), et supprimer une facture libère ses prestations (`pre_delete`) ;
  - le total d'une facture est la somme de ses prestations (`update_total`), recalculé quand l'une change (`post_save`) ;
  - une prestation se coche `billed` à la main, une fois facturée sur facture.net ; celle d'une ancienne facture ne se décoche pas (`Service.clean`).

  Un changement qui touche l'un d'eux garde les autres, prouvé par un test. Un `queryset.update()` saute `save()` et les signaux : il ne recalcule aucun total.
- Une règle de valeur vit dans le modèle (`clean`, contrainte), avec son message en français, pas dans la vue ni le formulaire : `number` unique, échéance après l'émission (`Invoice.clean`), prestation d'une ancienne facture toujours facturée (`Service.clean`).
- **Suppressions protégées** (`on_delete=PROTECT`) : un client, un projet ou une prestation encore référencés ne se suppriment pas. Le gabarit cache alors le bouton (`project.has_services`) ; appelée quand même, la suppression lève `ProtectedError`.
- **Formulaires** : `ModelForm` dans `customers/forms.py`, rendus par crispy-forms (`bootstrap5`), une date en `DateInput(attrs={"type": "date"}, format="%Y-%m-%d")` (sans `format`, la date s'écrit au format français, que le sélecteur de date du navigateur ne lit pas : le champ s'affiche vide). Une vue ou un formulaire nouveau liste ses champs (`fields = [...]`) : un champ ajouté au modèle ne devient pas éditable sans que Gabriel l'ait décidé.
- **Recherche par HTMX** (`search_view`, `search_results_view`) : la vue des résultats ne rend que le fragment que remplace `hx-target`.
- Les tests de ces vues se connectent par `client.force_login(admin)`, la fixture `admin` de `tests/conftest.py`.
