from rest_framework import serializers

from hello_world.models import User, SearchHistory



class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Acton list, model User"""
    class Meta:
        model = User
        fields = ["id", "email", "is_superuser", "is_active", "last_login", ]

class UserDetailsSerializer(serializers.ModelSerializer):
    """Action retrieve, model User"""
    class Meta:
        model = User
        exclude = ["password", ]


class CreateUserSerializer(serializers.ModelSerializer):
    """Action create, model User"""

    def create(self, *args, **kwargs):
        """Storing the password as a hash with the post method"""
        user = super().create(*args, **kwargs)
        not_hash_password = user.password
        user.set_password(not_hash_password)
        user.save()
        return user

    class Meta:
        model = User
        exclude = ["last_login", ]


class UpdateUserSerializerAdmin(serializers.ModelSerializer):
    """Action update for admin users, model User"""
    class Meta:
        model = User
        exclude = ["last_login", "password"]

class UpdateUserSerializerUser(serializers.ModelSerializer):
    """Action update for regular user, model User"""
    class Meta:
        model = User
        fields = ["email",]


class SearchHistorySerializer(serializers.ModelSerializer):
    """ For actions list and retrieve, model SearchHistory"""
    user = serializers.ReadOnlyField(source='user.email', )# output of the owner of the record in the form of his e-mail

    class Meta:
        model = SearchHistory
        fields = "__all__"


class SearchHistoryUnitSerializer(serializers.ModelSerializer):
    """For actions update, and destroy, model SearchHistory"""

    class Meta:
        model = SearchHistory
        exclude = ["user",]

class CreateSearchHistoryUnitSerializer(serializers.ModelSerializer):
    """For actions create, model SearchHistory"""

    class Meta:
        model = SearchHistory
        fields = "__all__"
