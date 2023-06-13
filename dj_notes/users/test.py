from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import User
from .views import UserUpdateView


class UserTest(TestCase):
    def setUp(self):
        self.user_data = {"username": "test1", "email": "test1@gmail.com"}
        user = User.objects.create(
            username="test1",
            email="test1@gmail.com",
        )
        self.user1 = user

    def create_user(
        self,
        username="test",
        email="test@test.com",
    ):

        return User.objects.create(
            username=username,
            email=email,
        )

    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__str__(), w.name)
