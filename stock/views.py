from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import calculer_stock


@login_required
def liste(request):
    stock = calculer_stock()
    return render(request, "stock/liste.html", {"stock": stock})
