from django import forms

from customers.models import Service


class ServiceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Service
        fields = ["date", "time_spent", "billed", "description"]
