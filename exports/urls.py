from django.urls import path
from . import views

app_name = "exports"

urlpatterns = [
    path("", views.index, name="index"),
    path("excel/<str:nom>/", views.export_excel, name="excel"),
    path("pdf/<str:nom>/", views.export_pdf, name="pdf"),
]
