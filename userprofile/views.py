from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


from .models import Profile
from account.permissions import IsOwner, IsVerifiedUser
from .serializers import ProfileUpdateSerializer, UserProfileSerializer


@extend_schema(summary='User profile View set', tags=['Profile'])
class ProfileViewSet(viewsets.ModelViewSet):
    '''This class is a viewset that allows you to create and update a user's profile'''
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsVerifiedUser)
    http_method_names = ('post', 'patch', 'head', 'options', 'trace',)
    lookup_field = 'slug'

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def perform_create(self, serializer):
        """
        Called during the creation of a new profile.
        Assigns the requesting user to the profile.
        """
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        kwargs['context'] = self.get_serializer_context()

        # Assign user from request.user to the profile
        request.data['user'] = request.user.id

        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        """
        If the action is create, then return the permissions IsAuthenticated() and IsVerifiedUser(),
        otherwise return the default permissions.
        """
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsVerifiedUser()]

        return super().get_permissions()



class UserProfileAPIView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get',)

    @extend_schema(summary="User all profile details", tags=["Profile"])
    def get(self, request):
        serialized = UserProfileSerializer(
            request.user, context={"request": request})
        data = serialized.data
        data['user_permissions'] = request.user.get_all_permissions()
        return Response({
            'results': data
        }, status=status.HTTP_200_OK)
