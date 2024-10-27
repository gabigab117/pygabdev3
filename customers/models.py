from django.db import models
from django.db.models import F, Sum


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    siret = models.CharField(max_length=14)
    address = models.CharField(max_length=200, verbose_name="Adresse", help_text="Rue")
    zip_code = models.CharField(max_length=20, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    created_at = models.DateField(verbose_name="Création de la fiche", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"


class Project(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Client", related_name="projects")
    name = models.CharField(verbose_name="Nom", max_length=100)
    hourly_rate = models.IntegerField(verbose_name="Taux horaire")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.customer}"

    class Meta:
        verbose_name = "Projet"


class Service(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name="Projet", related_name="services")
    date = models.DateField(verbose_name="Date de réalisation")
    time_spent = models.FloatField()
    billed = models.BooleanField(verbose_name="Réglé", default=False)
    description = models.TextField(blank=True)
    total = models.GeneratedField(expression=F("time_spent") * F("project__hourly_rate"),
                                  output_field=models.DecimalField(decimal_places=2), db_persist=True,
                                  verbose_name="Montant")

    def __str__(self):
        return f"{self.project} - {self.billed}"


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Client", related_name="invoices")
    number = models.IntegerField(unique=True, verbose_name="Numéro")
    issue_date = models.DateField(verbose_name="Date d'émission")
    delivery_date = models.DateField(verbose_name="Date de livraison")
    due_date = models.DateField(verbose_name="Date de d'échéance")
    services = models.ManyToManyField(Service)
    paid = models.BooleanField(verbose_name="Payé", default=False)
    total = models.GeneratedField(expression=Sum("services__total"), output_field=models.DecimalField(decimal_places=2),
                                  db_persist=True)
    pdf = models.FileField(upload_to="factures")

    def __str__(self):
        return f"{self.customer} - {self.number} - {self.issue_date} - {self.paid}"

    class Meta:
        verbose_name = "Facture"

    def clean(self):
        ...
