from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import LoginForm, EmployeCreationForm
from .decorators import admin_required
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or reverse("dashboard:index")
            return redirect(next_url)
        messages.error(request, _("Identifiant ou mot de passe incorrect."))

    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
@admin_required
def employes_liste(request):
    employes = User.objects.all().order_by("username")
    return render(request, "accounts/employes_liste.html", {"employes": employes})


@login_required
@admin_required
def employe_creer(request):
    form = EmployeCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Employé créé avec succès."))
        return redirect("accounts:employes_liste")
    return render(request, "accounts/employe_form.html", {"form": form})


@login_required
@admin_required
def employe_toggle_actif(request, pk):
    employe = get_object_or_404(User, pk=pk)
    if employe != request.user:
        employe.is_active = not employe.is_active
        employe.save(update_fields=["is_active"])
        messages.success(request, _("Statut de %(u)s mis à jour.") % {"u": employe.username})
    return redirect("accounts:employes_liste")
