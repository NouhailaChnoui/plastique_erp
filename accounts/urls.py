from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("employes/", views.employes_liste, name="employes_liste"),
    path("employes/nouveau/", views.employe_creer, name="employe_creer"),
    path("employes/<int:pk>/toggle/", views.employe_toggle_actif, name="employe_toggle"),
]
