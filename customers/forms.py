from django import forms
from django.db.models import Q

from customers.models import Service, Invoice


class ServiceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Service
        fields = ["date", "time_spent", "description"]


class InvoiceForm(forms.ModelForm):
    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Date d'émission",
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Date d'échéance",
    )
    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        label="Date de livraison",
    )

    class Meta:
        model = Invoice
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["services"].queryset = Service.objects.filter(billed=False)


class InvoiceUpdateForm(InvoiceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["services"].queryset = Service.objects.filter(
            Q(billed=False) | Q(invoices=self.instance)
        )
