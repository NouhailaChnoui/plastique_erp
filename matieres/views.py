from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Materiau
from .forms import MateriauForm


@login_required
def liste(request):
    materiaux = Materiau.objects.all()
    return render(request, "matieres/liste.html", {"materiaux": materiaux})


@login_required
def creer(request):
    form = MateriauForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Matière ajoutée avec succès."))
        return redirect("matieres:liste")
    return render(request, "matieres/form.html", {"form": form, "titre": _("Nouvelle matière")})


@login_required
def modifier(request, pk):
    materiau = get_object_or_404(Materiau, pk=pk)
    form = MateriauForm(request.POST or None, instance=materiau)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Matière mise à jour."))
        return redirect("matieres:liste")
    return render(request, "matieres/form.html", {"form": form, "titre": _("Modifier la matière")})


@login_required
def supprimer(request, pk):
    materiau = get_object_or_404(Materiau, pk=pk)
    if request.method == "POST":
        materiau.delete()
        messages.success(request, _("Matière supprimée."))
        return redirect("matieres:liste")
    return render(request, "matieres/confirm_delete.html", {"materiau": materiau})
