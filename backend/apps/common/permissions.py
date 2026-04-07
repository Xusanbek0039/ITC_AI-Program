from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level permission: only owner can access."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsVerifiedUser(BasePermission):
    """Only verified users can access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified
