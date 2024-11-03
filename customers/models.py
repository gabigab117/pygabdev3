from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    siret = models.CharField(max_length=14)
    address = models.CharField(max_length=200, verbose_name="Adresse", help_text="Rue")
    zip_code = models.CharField(max_length=20, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    created_at = models.DateField(verbose_name="Création de la fiche", auto_now_add=True)

    @property
    def has_unpaid(self):
        return Invoice.objects.filter(customer=self, paid=False).exists()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"

    def get_absolute_url(self):
        return reverse("customers:customer", kwargs={"pk": self.pk})


class Project(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Client", related_name="projects")
    name = models.CharField(verbose_name="Nom", max_length=100)
    hourly_rate = models.IntegerField(verbose_name="Taux horaire")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.customer}"

    class Meta:
        verbose_name = "Projet"

    def has_services(self):
        return self.services.exists()

    def get_absolute_url(self):
        return reverse("customers:project", kwargs={"pk": self.pk})


class Service(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name="Projet", related_name="services")
    date = models.DateField(verbose_name="Date de réalisation")
    time_spent = models.FloatField(help_text="En centièmes", verbose_name="Temps passé")
    billed = models.BooleanField(verbose_name="Facturé", default=False)
    description = models.TextField(blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=7, blank=True)

    def get_absolute_url(self):
        return reverse("customers:service", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.project} - {self.billed} - {self.total}"

    def save(self, *args, **kwargs):
        self.total = self.time_spent * self.project.hourly_rate
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date", "project__customer"]


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Client", related_name="invoices")
    number = models.IntegerField(unique=True, verbose_name="Numéro")
    issue_date = models.DateField(verbose_name="Date d'émission")
    delivery_date = models.DateField(verbose_name="Date de livraison")
    due_date = models.DateField(verbose_name="Date de d'échéance")
    services = models.ManyToManyField(Service, blank=True, related_name="invoices")
    paid = models.BooleanField(verbose_name="Payé", default=False)
    total = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    pdf = models.FileField(upload_to="factures", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("customers:invoice", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.customer} - {self.number} - {self.issue_date} - {self.paid}"

    class Meta:
        verbose_name = "Facture"
        ordering = ["-issue_date"]

    def clean(self):
        super().clean()
        if self.due_date <= self.issue_date:
            raise ValidationError({"due_date": "La date d'échéance ne peut pas être antérieure à la date d'émission"})

    def update_total(self):
        self.total = self.services.aggregate(total=Sum("total"))["total"] or 0
        self.save()


@receiver(m2m_changed, sender=Invoice.services.through)
def handle_invoice_change(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        Service.objects.filter(id__in=pk_set).update(billed=True)
    elif action == "post_remove":
        Service.objects.filter(id__in=pk_set).update(billed=False)
    elif action == "post_clear":
        instance .services.update(billed=False)
    instance.update_total()


@receiver(post_save, sender=Service)
def handle_service_change(sender, instance, **kwargs):
    invoice = instance.invoices.first()
    if invoice:
        invoice.update_total()
