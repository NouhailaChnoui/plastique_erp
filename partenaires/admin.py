from django.contrib import admin
from .models import Client, Fournisseur


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "ville")
    search_fields = ("nom", "telephone", "ville")


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "ville")
    search_fields = ("nom", "telephone", "ville")
