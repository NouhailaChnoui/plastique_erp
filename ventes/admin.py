from django.contrib import admin
from .models import Vente, PaiementVente, ChequeVente


class ChequeInline(admin.TabularInline):
    model = ChequeVente
    extra = 0


@admin.register(PaiementVente)
class PaiementVenteAdmin(admin.ModelAdmin):
    list_display = ("vente", "mode", "montant_total", "date_paiement")
    inlines = [ChequeInline]


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ("numero_facture", "client", "materiau", "quantite", "montant_total", "date_vente", "statut_paiement")
    list_filter = ("materiau", "date_vente")
    search_fields = ("numero_facture", "numero_bon", "client__nom")
