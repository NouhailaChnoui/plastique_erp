from django.urls import path
from . import views

app_name = "ventes"

urlpatterns = [
    path("", views.liste, name="liste"),
    path("nouveau/", views.creer, name="creer"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/modifier/", views.modifier, name="modifier"),
    path("<int:pk>/paiement/", views.paiement_creer, name="paiement_creer"),
    path("<int:pk>/facture.pdf", views.facture_pdf, name="facture_pdf"),
    path("cheque/<int:pk>/statut/", views.cheque_statut, name="cheque_statut"),
    path("facture-groupee.pdf", views.facture_groupee_pdf, name="facture_groupee_pdf"),
]
