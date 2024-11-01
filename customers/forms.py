from django import forms

from customers.models import Service


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ["date", "time_spent", "description"]
