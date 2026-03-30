# Python modules
from typing import Any

# Django modules
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateTimeField,
    ImageField,
)
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Project modules
from apps.abstracts.models import Abstact
# from apps.auths.validators import (
#     validate_email_domain,
#     validat  e_email_payload_not_in_full_name,
# )
class CustomUserManager(BaseUserManager):
    """
    Custom User Manager
    """
    def __obtain_user(
            self,
            email: str,
            first_name: str,
            last_name: str,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        if not email:
            raise ValidationError(
                message="no email"
            )
        if not first_name:
            raise ValidationError(
                message="no first name"
            )
        if not last_name:
            raise ValidationError(
                message="no last name"
            )
        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        return new_user

    def create_superuser(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str = None,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        if password:
            new_user.set_password(password)
        else:
            new_user.set_password("admin123")
        new_user.save(using=self._db)
        return new_user

    def create_user(
            self,
            email: str,
            first_name: str,
            last_name: str,
            password: str = None,
            **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        if password:
            new_user.set_password(password)
        else:
            new_user.set_password("admin123")
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, Abstact):
    """
        Custom user model extending AbstractBaseModel.
    """
    EMAIL_MAX_LENGTH = 150
    FIRST_NAME_MAX_LENGTH = 150

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        # validators=[validate_email_domain],
        verbose_name=_("Email Field"),
        help_text="User's email address",
    )
    first_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        verbose_name="First name",
    )
    last_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        verbose_name="Last name",
    )
    is_staff = BooleanField(
        default=True,
        verbose_name="Staff status",
        help_text="True if the user is an admin and has an access to the admin panel",
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="True if the user is active and has an access to request data",
    )

    date_joined = DateTimeField(
        auto_now_add=True,
    )

    image = ImageField()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    class Meta:
        """Meta options for CustomUser model."""

        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]

    def clean(self) -> None:
        """Validate the model instance before saving."""
        # validate_email_payload_not_in_full_name(
        #     email=self.email,
        #     full_name=self.full_name,
        # )
        return super().clean()