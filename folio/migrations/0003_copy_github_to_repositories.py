from django.db import migrations


def github_to_repositories(apps, schema_editor):
    FolioPage = apps.get_model("folio", "FolioPage")
    FolioRepository = apps.get_model("folio", "FolioRepository")
    FolioRepository.objects.bulk_create(
        FolioRepository(page=page, url=page.github, sort_order=0)
        for page in FolioPage.objects.exclude(github="")
    )


def repositories_to_github(apps, schema_editor):
    FolioRepository = apps.get_model("folio", "FolioRepository")
    for repo in FolioRepository.objects.order_by("-sort_order").select_related("page"):
        repo.page.github = repo.url
        repo.page.save(update_fields=["github"])


class Migration(migrations.Migration):
    dependencies = [
        ("folio", "0002_foliorepository"),
    ]

    operations = [
        migrations.RunPython(github_to_repositories, repositories_to_github),
    ]
