from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from .models import Vente, PaiementVente, ChequeVente
from .forms import VenteForm, PaiementVenteForm, ChequeVenteFormSet
from .pdf import generer_facture_pdf, generer_facture_groupee_pdf


@login_required
def liste(request):
    ventes = Vente.objects.select_related("client", "materiau").all()

    q = request.GET.get("q")
    statut = request.GET.get("statut")
    if q:
        ventes = ventes.filter(
            Q(numero_bon__icontains=q) | Q(numero_facture__icontains=q) |
            Q(client__nom__icontains=q) | Q(materiau__nom__icontains=q)
        )
    if statut:
        ventes = [v for v in ventes if v.statut_paiement_css == statut]

    return render(request, "ventes/liste.html", {"ventes": ventes, "q": q or "", "statut": statut or ""})


@login_required
def creer(request):
    form = VenteForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        vente = form.save(commit=False)
        vente.created_by = request.user
        vente.save()
        messages.success(request, _("Vente enregistrée. Facture %(facture)s générée.") % {"facture": vente.numero_facture})
        return redirect("ventes:detail", pk=vente.pk)
    return render(request, "ventes/form.html", {"form": form, "titre": _("Nouvelle vente")})


@login_required
def modifier(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    form = VenteForm(request.POST or None, request.FILES or None, instance=vente)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Vente mise à jour."))
        return redirect("ventes:detail", pk=vente.pk)
    return render(request, "ventes/form.html", {"form": form, "titre": _("Modifier la vente")})


@login_required
def detail(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    paiements = vente.paiements.all().prefetch_related("cheques")
    return render(request, "ventes/detail.html", {"vente": vente, "paiements": paiements})


@login_required
def paiement_creer(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    form = PaiementVenteForm(request.POST or None)
    formset = ChequeVenteFormSet(request.POST or None, request.FILES or None, prefix="cheques")

    if request.method == "POST" and form.is_valid():
        paiement = form.save(commit=False)
        paiement.vente = vente
        paiement.created_by = request.user

        needs_cheques = paiement.mode in ("cheque", "mixte")
        paiement.save()

        formset_ok = True
        if needs_cheques:
            formset = ChequeVenteFormSet(request.POST, request.FILES, instance=paiement, prefix="cheques")
            if formset.is_valid():
                formset.save()
            else:
                formset_ok = False

        if formset_ok:
            messages.success(request, _("Paiement enregistré avec succès."))
            return redirect("ventes:detail", pk=vente.pk)
        else:
            messages.error(request, _("Merci de vérifier les informations des chèques."))

    return render(request, "ventes/paiement_form.html", {"vente": vente, "form": form, "formset": formset})


@login_required
def facture_pdf(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    buffer = generer_facture_pdf(vente)
    response = HttpResponse(buffer, content_type="application/pdf")
    disposition = "inline" if request.GET.get("inline") else "attachment"
    response["Content-Disposition"] = f'{disposition}; filename="Facture_{vente.numero_facture}.pdf"'
    return response


@login_required
def cheque_statut(request, pk):
    cheque = get_object_or_404(ChequeVente, pk=pk)
    if request.method == "POST":
        nouveau_statut = request.POST.get("statut")
        if nouveau_statut in dict(ChequeVente.Statut.choices):
            cheque.statut = nouveau_statut
            cheque.save(update_fields=["statut"])
            messages.success(request, _("Statut du chèque mis à jour."))
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
    return redirect("ventes:detail", pk=cheque.paiement.vente.pk)


@login_required
def facture_groupee_pdf(request):
    ids = request.POST.getlist("vente_ids") or request.GET.getlist("vente_ids")
    if not ids:
        messages.error(request, _("Merci de sélectionner au moins une facture."))
        return redirect("ventes:liste")

    ventes = list(Vente.objects.filter(pk__in=ids).select_related("client", "materiau").order_by("date_vente"))
    if not ventes:
        messages.error(request, _("Aucune facture correspondante trouvée."))
        return redirect("ventes:liste")

    buffer = generer_facture_groupee_pdf(ventes)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Releve_ventes.pdf"'
    return response
