from django.contrib.auth.backends import ModelBackend
from users.models import Profile


class EmailAuthBackend(ModelBackend):
    """Authenticate using e-mail account."""

    def authenticate(self, username=None, email=None):
        try:
            user = Profile.objects.get(name=username)
            if user.check_email(email):
                return user
            return None
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
