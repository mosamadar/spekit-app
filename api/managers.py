from django.db import models
from soccer_app.utils import MessageResponse


class PlayersManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def check_is_transferred(self):
        """Returns only players which are not on transferred list'."""
        return self.filter(is_transferred=False)


class TransferManager(models.Manager):
    """Custom manager providing shortcuts for filtering by status."""

    def get_new_transferred(self):
        """Returns only players which are new on transfer list'."""
        return self.filter(status=MessageResponse.NEW.value)