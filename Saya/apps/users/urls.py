# Django Modules
from django.urls import path, include

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# project Modules
from apps.users.views import UserViewSet


router: DefaultRouter = DefaultRouter(
)

router.register(
    prefix="auth",
    viewset=UserViewSet,
    basename="auth",
)

urlpatterns = [
    # Пути из роутера: /auth/register/
    path("", include(router.urls)),

    # Ваши ручные пути
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]