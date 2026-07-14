from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="dashboard:index"), name="home"),
    path("accounts/", include("accounts.urls")),
    path("achats/", include("achats.urls")),
    path("ventes/", include("ventes.urls")),
    path("matieres/", include("matieres.urls")),
    path("stock/", include("stock.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("cheques/", include("cheques.urls")),
    path("partenaires/", include("partenaires.urls")),
    path("recherche/", include("recherche.urls")),
    path("exports/", include("exports.urls")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
