# Generated by Django 5.1.2 on 2024-10-27 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='billed',
            field=models.BooleanField(default=False, verbose_name='Facturé'),
        ),
    ]
