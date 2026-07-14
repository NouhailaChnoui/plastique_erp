from django.contrib import admin
from .models import Achat, PaiementAchat, ChequeAchat


class ChequeInline(admin.TabularInline):
    model = ChequeAchat
    extra = 0


@admin.register(PaiementAchat)
class PaiementAchatAdmin(admin.ModelAdmin):
    list_display = ("achat", "mode", "montant_total", "date_paiement")
    inlines = [ChequeInline]


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ("numero_bon", "numero_facture", "fournisseur", "materiau", "quantite", "montant_total", "date_achat", "statut_paiement")
    list_filter = ("materiau", "date_achat")
    search_fields = ("numero_bon", "numero_facture", "fournisseur__nom")
