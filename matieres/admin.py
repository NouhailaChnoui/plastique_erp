from django.contrib import admin
from .models import Materiau


@admin.register(Materiau)
class MateriauAdmin(admin.ModelAdmin):
    list_display = ("nom", "code", "actif", "date_creation")
    list_filter = ("actif",)
    search_fields = ("nom", "code")
