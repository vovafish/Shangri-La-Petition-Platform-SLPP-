from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

def jwt_required(view_func):
    @permission_classes([IsAuthenticated])
    @api_view(['GET', 'POST'])
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapped_view
