from decimal import Decimal
from datetime import timedelta
from django.conf import settings
from django.db.models import Sum, Count
from django.utils import timezone

from achats.models import Achat, ChequeAchat
from ventes.models import Vente, ChequeVente
from partenaires.models import Client, Fournisseur
from stock.services import calculer_stock


def get_notifications():
    """Construit la liste des notifications actives (badge navbar + panneau)."""
    today = timezone.localdate()
    limite = today + timedelta(days=settings.JOURS_ALERTE_CHEQUE)
    notifs = []

    cheques_a_payer = ChequeAchat.objects.filter(statut="attente", date_encaissement__lte=limite).select_related("paiement__achat__fournisseur")
    for c in cheques_a_payer[:10]:
        notifs.append({
            "message": f"Chèque {c.numero} à payer ({c.paiement.achat.fournisseur}) - {c.montant} DH le {c.date_encaissement}",
            "url": "/cheques/a-payer/",
            "icon": "fa-money-check",
            "level": "warning",
        })

    cheques_a_encaisser = ChequeVente.objects.filter(statut="attente", date_encaissement__lte=limite).select_related("paiement__vente__client")
    for c in cheques_a_encaisser[:10]:
        notifs.append({
            "message": f"Chèque {c.numero} à encaisser ({c.paiement.vente.client}) - {c.montant} DH le {c.date_encaissement}",
            "url": "/cheques/a-encaisser/",
            "icon": "fa-money-check-dollar",
            "level": "info",
        })

    for s in calculer_stock():
        if s["stock_faible"]:
            notifs.append({
                "message": f"Stock faible pour {s['materiau'].nom} : {s['stock_kg']:.0f} Kg restants",
                "url": "/stock/",
                "icon": "fa-triangle-exclamation",
                "level": "danger",
            })

    factures_impayees = Vente.objects.count()
    ventes_impayees = [v for v in Vente.objects.all() if v.statut_paiement != "Payé"]
    if ventes_impayees:
        notifs.append({
            "message": f"{len(ventes_impayees)} facture(s) non totalement réglée(s)",
            "url": "/ventes/?statut=non-paye",
            "icon": "fa-file-invoice-dollar",
            "level": "warning",
        })

    return notifs


def get_kpis():
    today = timezone.localdate()

    achats = Achat.objects.all()
    ventes = Vente.objects.all()

    total_achats = achats.aggregate(t=Sum("montant_total"))["t"] or Decimal("0")
    total_ventes = ventes.aggregate(t=Sum("montant_total"))["t"] or Decimal("0")

    stock = calculer_stock()
    stock_total_kg = sum((s["stock_kg"] for s in stock), Decimal("0"))

    creances_clients = sum((v.reste_a_recevoir for v in ventes), Decimal("0"))
    dettes_fournisseurs = sum((a.reste_a_payer for a in achats), Decimal("0"))

    cheques_en_attente = (
        ChequeAchat.objects.filter(statut="attente").count()
        + ChequeVente.objects.filter(statut="attente").count()
    )
    nb_cheques = ChequeAchat.objects.count() + ChequeVente.objects.count()

    return {
        "nb_achats": achats.count(),
        "nb_ventes": ventes.count(),
        "total_achats": total_achats,
        "total_ventes": total_ventes,
        "benefice": total_ventes - total_achats,
        "stock_total_kg": stock_total_kg,
        "nb_fournisseurs": Fournisseur.objects.count(),
        "nb_clients": Client.objects.count(),

        "achats_aujourdhui": achats.filter(date_achat=today).aggregate(t=Sum("montant_total"))["t"] or Decimal("0"),
        "ventes_aujourdhui": ventes.filter(date_vente=today).aggregate(t=Sum("montant_total"))["t"] or Decimal("0"),
        "chiffre_affaires": total_ventes,
        "depenses": total_achats,
        "profit": total_ventes - total_achats,
        "nb_cheques": nb_cheques,
        "cheques_en_attente": cheques_en_attente,
        "creances_clients": creances_clients,
        "dettes_fournisseurs": dettes_fournisseurs,
    }


def _mois_labels(n=6):
    today = timezone.localdate().replace(day=1)
    mois = []
    for i in range(n - 1, -1, -1):
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        mois.append((year, month))
    return mois


def get_chart_data():
    mois = _mois_labels(6)
    labels = [f"{m:02d}/{y}" for (y, m) in mois]

    achats_mensuels, ventes_mensuelles = [], []
    for (y, m) in mois:
        a = Achat.objects.filter(date_achat__year=y, date_achat__month=m).aggregate(t=Sum("montant_total"))["t"] or 0
        v = Vente.objects.filter(date_vente__year=y, date_vente__month=m).aggregate(t=Sum("montant_total"))["t"] or 0
        achats_mensuels.append(float(a))
        ventes_mensuelles.append(float(v))

    repartition = list(
        Vente.objects.values("materiau__nom").annotate(total=Sum("montant_total")).order_by("-total")[:8]
    )

    top_clients = list(
        Vente.objects.values("client__nom").annotate(total=Sum("montant_total")).order_by("-total")[:5]
    )
    top_fournisseurs = list(
        Achat.objects.values("fournisseur__nom").annotate(total=Sum("montant_total")).order_by("-total")[:5]
    )

    return {
        "labels": labels,
        "achats_mensuels": achats_mensuels,
        "ventes_mensuelles": ventes_mensuelles,
        "repartition_labels": [r["materiau__nom"] for r in repartition],
        "repartition_valeurs": [float(r["total"] or 0) for r in repartition],
        "top_clients_labels": [c["client__nom"] for c in top_clients],
        "top_clients_valeurs": [float(c["total"] or 0) for c in top_clients],
        "top_fournisseurs_labels": [f["fournisseur__nom"] for f in top_fournisseurs],
        "top_fournisseurs_valeurs": [float(f["total"] or 0) for f in top_fournisseurs],
    }
