def notifications_context(request):
    """
    Rend disponibles dans TOUS les templates :
      - le nombre de notifications actives (badge navbar)
      - le nom de l'entreprise
    Le calcul détaillé est fait par notifications.services pour éviter
    les imports circulaires et les requêtes coûteuses sur des pages qui
    n'en ont pas besoin (on ne calcule que le compteur ici).
    """
    from django.conf import settings

    data = {"nom_entreprise": settings.NOM_ENTREPRISE}

    if request.user.is_authenticated:
        try:
            from dashboard.services import get_notifications
            notifs = get_notifications()
            data["notifications"] = notifs
            data["notifications_count"] = len(notifs)
        except Exception:
            data["notifications"] = []
            data["notifications_count"] = 0

    return data
