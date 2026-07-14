from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
import re

LANG_PREFIX_RE = re.compile(r"^/(fr|ar)(/|$)")


class LoginRequiredMiddleware:
    """
    Redirige vers la page de connexion tout utilisateur non authentifié,
    sauf pour les URLs listées dans settings.LOGIN_EXEMPT_URLS
    (page de login, admin, fichiers statiques/media).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # On retire le préfixe de langue (/fr/, /ar/) pour comparer aux
        # URLs exemptées, car django.middleware.locale.LocaleMiddleware
        # ajoute ce préfixe automatiquement (i18n_patterns).
        path_sans_langue = LANG_PREFIX_RE.sub("/", path, count=1)

        exempt = any(path_sans_langue.startswith(url) for url in settings.LOGIN_EXEMPT_URLS)
        is_static = path.startswith(settings.STATIC_URL) or path.startswith(settings.MEDIA_URL)
        is_i18n = path.startswith("/i18n/")

        if not request.user.is_authenticated and not exempt and not is_static and not is_i18n:
            login_url = reverse("accounts:login")
            return redirect(f"{login_url}?next={path}")

        return self.get_response(request)
