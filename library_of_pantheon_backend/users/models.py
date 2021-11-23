from library_of_pantheon_backend.users.signals import user_pre_init_create_hash, user_pre_save_create_hash, user_post_save_handler
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    SET_NULL,
    OneToOneField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_init, pre_save, post_save

from library_of_pantheon_backend.utils.models import TimeStampAbstractModel, TimeStampAbstractModel, AbstractArchivedModel
from .types import USER_SETTING_TYPES, LIGHT


class UserSetting(TimeStampAbstractModel):
    mode = CharField(
        max_length=20,
        choices=USER_SETTING_TYPES,
        default=LIGHT,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.mode


class User(AbstractUser):
    """Default user for library-of-pantheon-backend."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=50)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    setting = OneToOneField(UserSetting, on_delete=SET_NULL, null=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


# pre_init.connect(user_pre_init_create_hash, sender=User)
# pre_save.connect(user_pre_save_create_hash, sender=User)
post_save.connect(user_post_save_handler, sender=User)
