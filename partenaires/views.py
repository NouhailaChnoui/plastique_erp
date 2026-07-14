from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Client, Fournisseur
from .forms import ClientForm, FournisseurForm


@login_required
def clients_liste(request):
    q = request.GET.get("q", "")
    clients = Client.objects.all()
    if q:
        clients = clients.filter(nom__icontains=q)
    return render(request, "partenaires/clients_liste.html", {"clients": clients, "q": q})


@login_required
def client_creer(request):
    form = ClientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Client ajouté avec succès."))
        return redirect("partenaires:clients_liste")
    return render(request, "partenaires/client_form.html", {"form": form, "titre": _("Nouveau client")})


@login_required
def client_modifier(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Client mis à jour."))
        return redirect("partenaires:clients_liste")
    return render(request, "partenaires/client_form.html", {"form": form, "titre": _("Modifier le client")})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    ventes = client.ventes.order_by("-date_vente")
    return render(request, "partenaires/client_detail.html", {"client": client, "ventes": ventes})


@login_required
def fournisseurs_liste(request):
    q = request.GET.get("q", "")
    fournisseurs = Fournisseur.objects.all()
    if q:
        fournisseurs = fournisseurs.filter(nom__icontains=q)
    return render(request, "partenaires/fournisseurs_liste.html", {"fournisseurs": fournisseurs, "q": q})


@login_required
def fournisseur_creer(request):
    form = FournisseurForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Fournisseur ajouté avec succès."))
        return redirect("partenaires:fournisseurs_liste")
    return render(request, "partenaires/fournisseur_form.html", {"form": form, "titre": _("Nouveau fournisseur")})


@login_required
def fournisseur_modifier(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    form = FournisseurForm(request.POST or None, instance=fournisseur)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Fournisseur mis à jour."))
        return redirect("partenaires:fournisseurs_liste")
    return render(request, "partenaires/fournisseur_form.html", {"form": form, "titre": _("Modifier le fournisseur")})


@login_required
def fournisseur_detail(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    achats = fournisseur.achats.order_by("-date_achat")
    return render(request, "partenaires/fournisseur_detail.html", {"fournisseur": fournisseur, "achats": achats})
