from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Restreint une vue au rôle Administrateur uniquement."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_admin):
            raise PermissionDenied("Accès réservé à l'administrateur.")
        return view_func(request, *args, **kwargs)
    return _wrapped
