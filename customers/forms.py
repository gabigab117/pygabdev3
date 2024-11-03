from django import forms

from customers.models import Service, Invoice


class ServiceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Service
        fields = ["date", "time_spent", "description"]


class InvoiceForm(forms.ModelForm):
    issue_date = forms.DateField(widget=forms.SelectDateWidget)
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    delivery_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Invoice
        fields = "__all__"
