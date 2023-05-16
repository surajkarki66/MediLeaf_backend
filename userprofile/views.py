from rest_framework import permissions, status, viewsets

from .models import Profile
from account.permissions import IsOwner, IsVerifiedUser
from .serializers import ProfileUpdateSerializer


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

    def get_permissions(self):
        """
        If the action is create, then return the permissions IsAuthenticated() and IsVerifiedUser(),
        otherwise return the default permissions
        :return: The permissions for the view.
        """
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsVerifiedUser()]

        return super().get_permissions()
