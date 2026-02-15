# Django modules
from django.urls import path, include

# Django REST Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from .views import PostViewSet

router = DefaultRouter()


router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]