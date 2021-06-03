from unittest import TestCase

from hello_world.models import User


class TestSerializers(TestCase):
    def test_users_list_serializer(self):
        self.user1 = User.objects.create_user(email="test1@gmail.com", password="123456")
        self.user2 = User.objects.create_user(email="test2@gmail.com", password="456123")
        self.user3 = User.objects.create_superuser(email="test3@gmail.com", password="55555")
