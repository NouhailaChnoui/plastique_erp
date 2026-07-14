from django.urls import path
from . import views

app_name = "cheques"

urlpatterns = [
    path("a-payer/", views.a_payer, name="a_payer"),
    path("a-encaisser/", views.a_encaisser, name="a_encaisser"),
]
