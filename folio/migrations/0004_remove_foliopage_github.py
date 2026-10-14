from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("folio", "0003_copy_github_to_repositories"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="foliopage",
            name="github",
        ),
    ]
