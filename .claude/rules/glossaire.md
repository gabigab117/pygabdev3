---
paths:
  - "**/*.py"
  - "**/templates/**/*.html"
---

# Glossaire FR → code

La table de référence. Sa règle d'usage est dans le CLAUDE.md (Conventions) : un mot nouveau y entre avant d'être utilisé.

## Back-office

| Français | Code |
|---|---|
| client | `customer` (`Customer`) |
| SIRET | `siret` |
| date de création de la fiche client | `created_at` |
| projet (d'un client, facturé au taux horaire) | `project` (`Project`). Un projet présenté sur le site est une réalisation, `FolioPage` |
| taux horaire | `hourly_rate` |
| prestation (du temps passé sur un projet, à facturer) | `service` (`Service`) |
| temps passé | `time_spent` |
| facturée (une prestation cochée une fois facturée sur facture.net, ou rattachée à une ancienne facture) | `billed` |
| facture (archivée : les nouvelles se font sur facture.net) | `invoice` (`Invoice`) |
| numéro (d'une facture) | `number` |
| date d'émission / de livraison / d'échéance | `issue_date` / `delivery_date` / `due_date` |
| payée | `paid` |
| montant total | `total` |
| tableau de bord | `dashboard` |
| recherche (du back-office) | `search` |

## Site public

| Français | Code |
|---|---|
| page (Wagtail) | `page` |
| page générique (abstraite : un en-tête) | `GenericPage` |
| en-tête (le texte d'introduction d'une page) | `header` |
| corps | `body` |
| image principale | `main_image` |
| date de publication | `date` |
| accueil | `home` (`HomePage`) |
| blog, article | `blog` : `BlogIndexPage`, `BlogPage` |
| étiquette (d'un article) | `tag` (`BlogTagIndexPage` liste les articles d'une étiquette) |
| réalisations, réalisation (un projet présenté sur le site) | `folio` : `FolioIndexPage`, `FolioPage` |
| dépôt GitHub (d'une réalisation, quatre au plus) | `repository` (`FolioRepository`) |
| libellé (d'un dépôt) | `label` |
| page de contact, ses champs | `FormPage`, `FormField` |
| page légale | `LegalPage` |
| bloc d'un corps : paragraphe, code | `paragraphe`, `code` (des clés stockées : elles restent telles quelles) |
| recherche (du site) | `search` |

## Comptes

| Français | Code |
|---|---|
| compte | `user` (`CustomUser`, `AUTH_USER_MODEL`) |
| staff (accès au back-office) | `is_staff` |
| compte de démonstration (local, fictif) | `demo` |
