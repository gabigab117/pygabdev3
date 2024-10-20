# Generated by Django 5.1.2 on 2024-10-19 16:15

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolioIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('header', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FolioPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('header', wagtail.fields.RichTextField(blank=True)),
                ('date', models.DateField(verbose_name='Date de publication')),
                ('body', wagtail.fields.StreamField([('paragraphe', 0), ('code', 3)], block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], 'help_text': 'Coding language', 'identifier': 'language', 'label': 'Language'}), 2: ('wagtail.blocks.TextBlock', (), {'identifier': 'code', 'label': 'Code'}), 3: ('wagtail.blocks.StructBlock', [[('language', 1), ('code', 2)]], {})})),
                ('youtube', models.URLField(blank=True, verbose_name='Lien Youtube')),
                ('github', models.URLField(blank=True, verbose_name='Lien GitHub')),
                ('production', models.URLField(blank=True, verbose_name='Lien du Projet')),
                ('main_image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image', verbose_name='Image principale')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]