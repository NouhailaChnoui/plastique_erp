from django import forms
from .models import Materiau


class MateriauForm(forms.ModelForm):
    class Meta:
        model = Materiau
        fields = ["nom", "code", "actif"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: PET Bleu"}),
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Généré automatiquement si vide"}),
            "actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
