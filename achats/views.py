from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from .models import Achat, ChequeAchat
from .forms import AchatForm, PaiementAchatForm, ChequeAchatFormSet
from .pdf import generer_facture_pdf, generer_facture_groupee_pdf


@login_required
def liste(request):
    achats = Achat.objects.select_related("fournisseur", "materiau").all()

    q = request.GET.get("q")
    statut = request.GET.get("statut")
    if q:
        achats = achats.filter(
            Q(numero_bon__icontains=q) | Q(numero_facture__icontains=q) |
            Q(fournisseur__nom__icontains=q) | Q(materiau__nom__icontains=q)
        )
    if statut:
        achats = [a for a in achats if a.statut_paiement_css == statut]

    return render(request, "achats/liste.html", {"achats": achats, "q": q or "", "statut": statut or ""})


@login_required
def creer(request):
    form = AchatForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        achat = form.save(commit=False)
        achat.created_by = request.user
        achat.save()
        messages.success(request, _("Achat enregistré. Facture %(facture)s générée. Montant total : %(montant)s DH") % {"facture": achat.numero_facture, "montant": achat.montant_total})
        return redirect("achats:detail", pk=achat.pk)
    return render(request, "achats/form.html", {"form": form, "titre": _("Nouvel achat")})


@login_required
def modifier(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    form = AchatForm(request.POST or None, request.FILES or None, instance=achat)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Achat mis à jour."))
        return redirect("achats:detail", pk=achat.pk)
    return render(request, "achats/form.html", {"form": form, "titre": _("Modifier l'achat")})


@login_required
def detail(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    paiements = achat.paiements.all().prefetch_related("cheques")
    return render(request, "achats/detail.html", {"achat": achat, "paiements": paiements})


@login_required
def paiement_creer(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    form = PaiementAchatForm(request.POST or None)
    formset = ChequeAchatFormSet(request.POST or None, request.FILES or None, prefix="cheques")

    if request.method == "POST" and form.is_valid():
        paiement = form.save(commit=False)
        paiement.achat = achat
        paiement.created_by = request.user

        needs_cheques = paiement.mode in ("cheque", "mixte")
        paiement.save()

        formset_ok = True
        if needs_cheques:
            formset = ChequeAchatFormSet(request.POST, request.FILES, instance=paiement, prefix="cheques")
            if formset.is_valid():
                formset.save()
            else:
                formset_ok = False

        if formset_ok:
            messages.success(request, _("Paiement enregistré avec succès."))
            return redirect("achats:detail", pk=achat.pk)
        else:
            messages.error(request, _("Merci de vérifier les informations des chèques."))

    return render(request, "achats/paiement_form.html", {"achat": achat, "form": form, "formset": formset})


@login_required
def facture_pdf(request, pk):
    achat = get_object_or_404(Achat, pk=pk)
    buffer = generer_facture_pdf(achat)
    response = HttpResponse(buffer, content_type="application/pdf")
    disposition = "inline" if request.GET.get("inline") else "attachment"
    response["Content-Disposition"] = f'{disposition}; filename="Facture_{achat.numero_facture}.pdf"'
    return response


@login_required
def cheque_statut(request, pk):
    cheque = get_object_or_404(ChequeAchat, pk=pk)
    if request.method == "POST":
        nouveau_statut = request.POST.get("statut")
        if nouveau_statut in dict(ChequeAchat.Statut.choices):
            cheque.statut = nouveau_statut
            cheque.save(update_fields=["statut"])
            messages.success(request, _("Statut du chèque mis à jour."))
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
    return redirect("achats:detail", pk=cheque.paiement.achat.pk)


@login_required
def facture_groupee_pdf(request):
    ids = request.POST.getlist("achat_ids") or request.GET.getlist("achat_ids")
    if not ids:
        messages.error(request, _("Merci de sélectionner au moins une facture."))
        return redirect("achats:liste")

    achats = list(Achat.objects.filter(pk__in=ids).select_related("fournisseur", "materiau").order_by("date_achat"))
    if not achats:
        messages.error(request, _("Aucune facture correspondante trouvée."))
        return redirect("achats:liste")

    buffer = generer_facture_groupee_pdf(achats)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Releve_achats.pdf"'
    return response
