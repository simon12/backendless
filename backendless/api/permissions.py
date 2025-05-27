from rest_framework import permissions

class IsEndpointOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an endpoint to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the endpoint
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # If the object is a TestArea, check if the user is the owner of the related endpoint
        if hasattr(obj, 'endpoint'):
            return obj.endpoint.user == request.user
        return False

class IsApiKeyOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an API key to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the API key
        return obj.user == request.user

class IsDrinkRoundCreator(permissions.BasePermission):
    """
    Custom permission to only allow creators of a drink round to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the creator of the drink round
        return obj.creator == request.user

class CanAccessDrinkRound(permissions.BasePermission):
    """
    Custom permission to allow access to a drink round if it's active and not expired.
    """
    def has_object_permission(self, request, view, obj):
        # Creators can always access their own drink rounds
        if obj.creator == request.user:
            return True
            
        # For others, check if the drink round is available
        return obj.is_available()
