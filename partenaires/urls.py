from django.urls import path
from . import views

app_name = "partenaires"

urlpatterns = [
    path("clients/", views.clients_liste, name="clients_liste"),
    path("clients/nouveau/", views.client_creer, name="client_creer"),
    path("clients/<int:pk>/", views.client_detail, name="client_detail"),
    path("clients/<int:pk>/modifier/", views.client_modifier, name="client_modifier"),

    path("fournisseurs/", views.fournisseurs_liste, name="fournisseurs_liste"),
    path("fournisseurs/nouveau/", views.fournisseur_creer, name="fournisseur_creer"),
    path("fournisseurs/<int:pk>/", views.fournisseur_detail, name="fournisseur_detail"),
    path("fournisseurs/<int:pk>/modifier/", views.fournisseur_modifier, name="fournisseur_modifier"),
]
