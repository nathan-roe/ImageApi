from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token


TOKEN_EXPIRE_TIME = timedelta(minutes=15)


class ExpiringToken(Token):
    """Extend Token to add expired method."""

    class Meta(object):
        proxy=True

    def expired(self):
        """Return boolean indicating token expiration."""
        now = timezone.now()
        if self.created < now - TOKEN_EXPIRE_TIME:
            return True
        return False
