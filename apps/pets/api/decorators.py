from rest_framework.response import Response
from rest_framework.views import status
from django.core.exceptions import ObjectDoesNotExist
from apps.users.models import User
from rest_framework import permissions

def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get("name", "")
        artist = args[0].request.data.get("zip_code", "")
        if not title and not artist:
            return Response(
                data={
                    "message": "Both name and zip code are required to add a city"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated

class IsSeller(permissions.BasePermission):
    message = 'You are not a owner'

    def has_permission(self, request, view):
        try:
            if request.user.is_staff:
                return True
            seller = User.objects.get(id=request.user.id)
            request.user.__dict__['seller'] = seller
        except ObjectDoesNotExist:
            return False
        else:
            return True
        
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.is_staff:
                return True
            owner = User.objects.get(id=request.user.id)
            request.user.__dict__['owner'] = owner
        except ObjectDoesNotExist:
            return False
        else:
            return True
