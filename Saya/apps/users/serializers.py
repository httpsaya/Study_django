# Python modules
from typing import Any, Optional

# Django REST Framework
from rest_framework.serializers import (
    Serializer,
    CharField,
    EmailField
)
from rest_framework.exceptions import ValidationError


# Project modules
from apps.users.models import CustomUser

class UserLoginSerializer(Serializer):
    """
    Serializer for user login.
    """

    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH,
    )
    password = CharField(
        required=True,
        max_length=CustomUser.FIRST_NAME_MAX_LENGTH,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates the input data."""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={
                    "email": [f"User with email '{email}' does not exist."]
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(
                detail={
                    "password": ["Incorrect password."]
                }
            )

        attrs["user"] = user

        return super().validate(attrs)


class UserRegisterSerializer(Serializer):
    """ User's login Serializer """

    email = EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH,
    )
    first_name = CharField(
        required=True,
        max_length=CustomUser.FIRST_NAME_MAX_LENGTH
    )
    last_name = CharField(
        required=True,
        max_length=CustomUser.FIRST_NAME_MAX_LENGTH
    )
    password = CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        Model = CustomUser
        """
        Validations of Serializer
        """

        fields = ('email', 'password' ,'first_name', 'last_name')

    def validate(
            self,
            attrs: dict[str, Any],
    ) -> dict[str, Any]:
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)