from rest_framework.permissions import BasePermission


class IsAuthentication(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)


class IsAuthenticatedAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.author)