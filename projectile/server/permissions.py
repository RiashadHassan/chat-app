from rest_framework import exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from projectile.server.models import Server
from projectile.member.models import Member


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        server_uid: str = str(view.kwargs.get("server_uid"))
        server = get_object_or_404(Server, uid=server_uid)
        if server.owner == request.user:
            return True
        return False


class IsMember(BasePermission):
    def has_permission(self, request, view):
        server_uid: str = str(view.kwargs.get("server_uid"))
        try:
            member = Member.objects.get(
                server_uid=server_uid,
                user_uid=request.user.uid,
            )
            if member.is_deleted:
                raise exceptions.PermissionDenied(
                    detail="You are no longer a member of this server."
                )
            return True
        except Member.DoesNotExist:
            raise exceptions.PermissionDenied(
                detail="You are not a member of this server."
            )


class IsMemberCached(BasePermission):
    def has_permission(self, request, view):
        server_uid: str = str(view.kwargs.get("server_uid"))
        data: dict = request.user.server_data.get(server_uid, {})
        if not data:
            return False
        if data.get("is_member") == True:
            return True
        else:
            raise exceptions.PermissionDenied(
                detail="You are no longer a member of this server."
            )
