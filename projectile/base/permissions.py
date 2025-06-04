from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class OrPermission:
    def __init__(self, *permission_classes):
        self.permission_classes = permission_classes

    def __call__(self):
        permission_classes = self.permission_classes

        class _OrPermission(BasePermission):
            def has_permission(self, request, view):
                return any(
                    perm().has_permission(request, view) for perm in permission_classes
                )

            def has_object_permission(self, request, view, obj):
                return any(
                    perm().has_object_permission(request, view, obj)
                    for perm in permission_classes
                )

        return _OrPermission()
