from decimal import Decimal
from django.conf import settings
from django.db.models import Sum
from matieres.models import Materiau
from achats.models import Achat
from ventes.models import Vente


def calculer_stock():
    """
    Calcule, pour chaque matière, le stock disponible en Kg :
    Stock = Total acheté (Kg) - Total vendu (Kg)
    """
    resultats = []
    for materiau in Materiau.objects.all():
        qte_achetee = Achat.objects.filter(materiau=materiau).aggregate(total=Sum("quantite"))["total"] or Decimal("0")
        qte_vendue = Vente.objects.filter(materiau=materiau).aggregate(total=Sum("quantite"))["total"] or Decimal("0")

        stock_kg = qte_achetee - qte_vendue
        resultats.append({
            "materiau": materiau,
            "quantite_achetee_kg": qte_achetee,
            "quantite_vendue_kg": qte_vendue,
            "stock_kg": stock_kg,
            "stock_faible": stock_kg < Decimal(str(settings.SEUIL_STOCK_FAIBLE_KG)),
        })
    return resultats
