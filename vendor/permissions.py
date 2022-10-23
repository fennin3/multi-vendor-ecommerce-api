from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsVendor(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_authenticated and \
                request.user.is_confirmed and request.user.user_type == 'VENDOR' and request.user.vendor !=None and not request.user.vendor.suspended) or (request.user and request.user.is_authenticated and \
                    request.user.user_type == 'ADMIN')
        )

class IsVendor2(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return bool(
            (request.user and request.user.is_authenticated and \
                request.user.is_confirmed and request.user.user_type == 'VENDOR' and request.user.vendor !=None and not request.user.vendor.suspended) or (request.user and request.user.is_authenticated and \
                    request.user.user_type == 'ADMIN')
        )


class IsUser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
        request.user and request.user.is_authenticated and request.user.is_confirmed)
