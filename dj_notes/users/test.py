from django.test import TestCase
from .models import User


class UserTest(TestCase):
    def create_user(
        self,
        username="test",
        email="test@test.com",
    ):

        return User.objects.create(
            username=username,
            email=email,  # password1="12345678", password2="12345678"
        )

    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__str__(), w.name)
