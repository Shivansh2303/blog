# from django.contib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class EmailAuthBackend:
    def authenticate(email,password):
        try:
            user=User.objects.get(email=email)
            success=user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            return None
        return None

