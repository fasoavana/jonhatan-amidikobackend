from rest_framework.permissions import BasePermission

#from .choices import UserRole
from .choices import UserRole, UserStatus


class IsAdmin(BasePermission):
    """
    Autorise uniquement les utilisateurs ayant le rôle admin.
    """

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role == UserRole.ADMIN
            and user.status == UserStatus.ACTIVE
            and user.is_active
        )

class IsModerator(BasePermission):
    """
    Autorise uniquement les modérateurs actifs.
    """

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role == UserRole.MODERATOR
            and user.status == UserStatus.ACTIVE
            and user.is_active
        )

class IsAdminOrModerator(BasePermission):
    """
    Autorise les administrateurs et les modérateurs actifs.
    """

    def has_permission(self, request, view):
        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role in [UserRole.ADMIN, UserRole.MODERATOR]
            and user.status == UserStatus.ACTIVE
            and user.is_active
        )
