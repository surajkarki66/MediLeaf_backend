from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        raise PermissionDenied(
            {"message": "You have no permission to perform this action"})


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an account to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj == request.user:
            return True
        raise PermissionDenied(
            {"message": "You have no permission to perform this action."})


class IsVerifiedUser(permissions.BasePermission):
    """
    Custom permission to only allow verified owners of an account to edit it.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_active and request.user.is_verified:
            return True
        raise PermissionDenied(
            {"message": "Please verify your profile to perform this action"})
