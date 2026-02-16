# Python modules
from typing import Any
from rest_framework_simplejwt.tokens import RefreshToken

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

# Project modules
from apps.users.models import CustomUser
from apps.users.serializers import UserLoginSerializer, UserRegisterSerializer

# Loggers
import logging
logger = logging.getLogger('users')


class UserViewSet(ViewSet):

    @action(
        methods=("POST",),
        detail=False,
        url_path='register',
        url_name='register',
        permission_classes=(AllowAny,)
    )
    def register(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any],
    ) -> DRFResponse:
        """ Doing registration endpoint """

        email = request.data.get("email")
        logger.info("Registration attempt for email: %s", email)

        try:
            serializer: UserRegisterSerializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()

            logger.info("User registered successfully: %s", user.email)

            refresh_token: RefreshToken = RefreshToken.for_user(user)
            access_token: str = str(refresh_token.access_token)

            return DRFResponse(
                data={
                    'first_name': user.first_name,
                    'access': access_token,
                    'refresh': str(refresh_token)
                },
                status=HTTP_200_OK
            )

        except ValidationError as e:
            logger.warning(
                "Registration failed for email: %s | Errors: %s",
                email,
                str(e)
            )
            raise

        except Exception:
            logger.exception("Unexpected error during registration for email: %s", email)
            raise

    @action(
        methods=("POST",),
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=(AllowAny,)
    )
    def login(
            self,
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle user login.
        """
        email = request.data.get("email")
        logger.info("Login attempt for email: %s", email)

        try:
            serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user: CustomUser = serializer.validated_data.pop("user")

            logger.info("Login successful for email: %s", user.email)

            refresh_token: RefreshToken = RefreshToken.for_user(user)
            access_token: str = str(refresh_token.access_token)

            return DRFResponse(
                data={
                    "id": user.id,
                    "email": user.email,
                    "access": access_token,
                    "refresh": str(refresh_token),
                },
                status=HTTP_200_OK
            )

        except ValidationError as e:
            logger.warning(
                "Login failed for email: %s | Errors: %s",
                email,
                str(e)
            )
            raise

        except Exception:
            logger.exception("Unexpected error during login for email: %s", email)
            raise