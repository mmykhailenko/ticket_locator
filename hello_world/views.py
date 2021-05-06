from rest_framework import viewsets, permissions

from hello_world.permissions import IsOwnerUserOrAdminOrReadOnly, IsOwnerHistoryOrReadOnly
from hello_world.models import User, SearchHistory
from hello_world.serializers import UserSerializer, UserDetailsSerializer, CreateUserSerializer, \
    SearchHistorySerializer, SearchHistoryUnitSerializer, UpdateUserSerializerAdmin, UpdateUserSerializerUser, \
    CreateSearchHistoryUnitSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes_by_action = {'create': [permissions.IsAdminUser],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [IsOwnerUserOrAdminOrReadOnly], }

    def serializer_change_for_update(self):
        """Depending on the status of the user (admin / regular user),
        different serializers are applied to the post method"""
        if self.request.user.is_superuser == True:
            return UpdateUserSerializerAdmin
        return UpdateUserSerializerUser

    def get_serializer_class(self):
        """Definition of the Sirializer depending on the http method"""
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action == 'retrieve':
            return UserDetailsSerializer
        elif self.action == 'update':
            return self.serializer_change_for_update()
        return UserSerializer

    def get_permissions(self):
        """Return permission_classes depending on `action or default permission_classes"""
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerHistoryOrReadOnly]

    def get_serializer_class(self):
        """Definition of the Sirializer depending on the http method"""
        if self.action == 'list':
            return SearchHistorySerializer
        elif self.action == 'retrieve':
            return SearchHistorySerializer
        elif self.action == 'create':
            return CreateSearchHistoryUnitSerializer
        return SearchHistoryUnitSerializer
