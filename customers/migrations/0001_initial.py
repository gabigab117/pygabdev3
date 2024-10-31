# Generated by Django 5.1.2 on 2024-10-27 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('siret', models.CharField(max_length=14)),
                ('address', models.CharField(help_text='Rue', max_length=200, verbose_name='Adresse')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Code postal')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Création de la fiche')),
            ],
            options={
                'verbose_name': 'Client',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('hourly_rate', models.IntegerField(verbose_name='Taux horaire')),
                ('description', models.TextField(blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='customers.customer', verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Projet',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date de réalisation')),
                ('time_spent', models.FloatField(help_text='En centièmes', verbose_name='Temps passé')),
                ('billed', models.BooleanField(default=False, verbose_name='Réglé')),
                ('description', models.TextField(blank=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=7)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='customers.project', verbose_name='Projet')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True, verbose_name='Numéro')),
                ('issue_date', models.DateField(verbose_name="Date d'émission")),
                ('delivery_date', models.DateField(verbose_name='Date de livraison')),
                ('due_date', models.DateField(verbose_name="Date de d'échéance")),
                ('paid', models.BooleanField(default=False, verbose_name='Payé')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('pdf', models.FileField(upload_to='factures')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='customers.customer', verbose_name='Client')),
                ('services', models.ManyToManyField(to='customers.service')),
            ],
            options={
                'verbose_name': 'Facture',
            },
        ),
    ]