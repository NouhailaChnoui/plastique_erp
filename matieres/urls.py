from django.urls import path
from . import views

app_name = "matieres"

urlpatterns = [
    path("", views.liste, name="liste"),
    path("nouveau/", views.creer, name="creer"),
    path("<int:pk>/modifier/", views.modifier, name="modifier"),
    path("<int:pk>/supprimer/", views.supprimer, name="supprimer"),
]
