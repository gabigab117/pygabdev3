# Generated by Django 5.1.2 on 2024-10-08 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_homepage_head'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='head',
            new_name='header',
        ),
    ]
