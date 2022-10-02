from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsSuperuser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated \
                and request.user.is_superuser
        )

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        ...