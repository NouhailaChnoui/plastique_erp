from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from partenaires.models import Client, Fournisseur
from matieres.models import Materiau
from achats.models import Achat
from ventes.models import Vente


@login_required
def index(request):
    q = request.GET.get("q", "").strip()
    resultats = {"clients": [], "fournisseurs": [], "materiaux": [], "achats": [], "ventes": []}

    if q:
        resultats["clients"] = Client.objects.filter(
            Q(nom__icontains=q) | Q(telephone__icontains=q) | Q(ville__icontains=q)
        )[:20]
        resultats["fournisseurs"] = Fournisseur.objects.filter(
            Q(nom__icontains=q) | Q(telephone__icontains=q) | Q(ville__icontains=q)
        )[:20]
        resultats["materiaux"] = Materiau.objects.filter(nom__icontains=q)[:20]
        resultats["achats"] = Achat.objects.filter(
            Q(numero_bon__icontains=q) | Q(fournisseur__nom__icontains=q) | Q(materiau__nom__icontains=q)
        ).select_related("fournisseur", "materiau")[:20]
        resultats["ventes"] = Vente.objects.filter(
            Q(numero_bon__icontains=q) | Q(numero_facture__icontains=q) |
            Q(client__nom__icontains=q) | Q(materiau__nom__icontains=q)
        ).select_related("client", "materiau")[:20]

    total = sum(len(v) for v in resultats.values())
    return render(request, "recherche/index.html", {"q": q, "resultats": resultats, "total": total})
