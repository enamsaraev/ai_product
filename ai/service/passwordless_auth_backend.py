from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class PasswordlessAuthBackend(ModelBackend):
    def authenticate(self, request, username=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return User.objects.create(username=username)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None