from django import forms
from .models import Client, Fournisseur

_widgets = {
    "nom": forms.TextInput(attrs={"class": "form-control"}),
    "telephone": forms.TextInput(attrs={"class": "form-control"}),
    "ville": forms.TextInput(attrs={"class": "form-control"}),
    "adresse": forms.TextInput(attrs={"class": "form-control"}),
}


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "telephone", "ville", "adresse"]
        widgets = _widgets


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ["nom", "telephone", "ville", "adresse"]
        widgets = _widgets
