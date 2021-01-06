from rest_framework.permissions import BasePermission


class InspectorPermission(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.auth is None:
            return False
        return request.auth['inspector']['is_enable']
