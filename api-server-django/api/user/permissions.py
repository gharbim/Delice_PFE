from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """Grants access only to Django superusers for account management."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )
