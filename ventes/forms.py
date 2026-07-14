from django import forms
from django.forms import inlineformset_factory
from .models import Vente, PaiementVente, ChequeVente


class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ["client", "materiau", "quantite", "prix_unitaire",
                  "date_vente", "numero_bon", "photo_bon", "observations"]
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "materiau": forms.Select(attrs={"class": "form-select"}),
            "quantite": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "id": "id_quantite"}),
            "prix_unitaire": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "id": "id_prix_unitaire"}),
            "date_vente": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "numero_bon": forms.TextInput(attrs={"class": "form-control"}),
            "photo_bon": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "observations": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class PaiementVenteForm(forms.ModelForm):
    class Meta:
        model = PaiementVente
        fields = ["mode", "montant_especes", "date_paiement"]
        widgets = {
            "mode": forms.Select(attrs={"class": "form-select", "id": "id_mode"}),
            "montant_especes": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "date_paiement": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


ChequeVenteFormSet = inlineformset_factory(
    PaiementVente, ChequeVente,
    fields=["numero", "banque", "montant", "date_encaissement", "photo", "statut"],
    extra=1, can_delete=True,
    widgets={
        "numero": forms.TextInput(attrs={"class": "form-control", "placeholder": "N° chèque"}),
        "banque": forms.TextInput(attrs={"class": "form-control", "placeholder": "Banque"}),
        "montant": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Montant"}),
        "date_encaissement": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        "statut": forms.Select(attrs={"class": "form-select"}),
    }
)
