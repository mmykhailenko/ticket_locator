from rest_framework import permissions

class IsOwnerUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows you to work with the object or the owner or admin
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser == True:
            return True
        return obj.email == request.user.email

class IsOwnerHistoryOrReadOnly(permissions.BasePermission):
    """
    Custom permission allowing only the owner of the flight history to delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
