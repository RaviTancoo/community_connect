from rest_framework import permissions


class IsOrganizationOwner(permissions.BasePermission):
    """
    Only the organization that created the opportunity can edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.organization
