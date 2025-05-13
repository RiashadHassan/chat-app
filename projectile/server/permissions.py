from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from projectile.server.models import Server


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        uid = view.kwargs.get("uid")
        server = get_object_or_404(Server, uid=uid)
        data = server.server_data.get("owner")
        if data and str(request.user.uid) in data:
            return True
        return False
