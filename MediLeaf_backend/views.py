from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    data = {
        "success": True,
        "message": "MediLeaf API is up and running!"
    }
    return Response(data, status.HTTP_200_OK)
