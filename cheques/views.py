from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from achats.models import ChequeAchat
from ventes.models import ChequeVente


def _filtrer_par_periode(queryset, periode, champ="date_encaissement"):
    today = timezone.localdate()
    if periode == "aujourdhui":
        return queryset.filter(**{champ: today})
    if periode == "semaine":
        fin = today + timedelta(days=7)
        return queryset.filter(**{f"{champ}__range": (today, fin)})
    if periode == "mois":
        fin = today + timedelta(days=30)
        return queryset.filter(**{f"{champ}__range": (today, fin)})
    return queryset


@login_required
def a_payer(request):
    periode = request.GET.get("periode", "")
    cheques = ChequeAchat.objects.select_related("paiement__achat__fournisseur").filter(statut="attente")
    cheques = _filtrer_par_periode(cheques, periode).order_by("date_encaissement")
    return render(request, "cheques/a_payer.html", {"cheques": cheques, "periode": periode})


@login_required
def a_encaisser(request):
    periode = request.GET.get("periode", "")
    cheques = ChequeVente.objects.select_related("paiement__vente__client").filter(statut="attente")
    cheques = _filtrer_par_periode(cheques, periode).order_by("date_encaissement")
    return render(request, "cheques/a_encaisser.html", {"cheques": cheques, "periode": periode})
