# Python modules
from typing import Any

# Django modules
from django.db.models import QuerySet, Count
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.decorators import action

# Project modules
from apps.blog.models import Post, Comment
from apps.blog.serializers import (
    PostBaseSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CommentSerializer,
)


class PostViewSet(ViewSet):
    """
    ViewSet для обработки эндпоинтов постов без использования декораторов.
    """
    permission_classes = [IsAuthenticated]  # Добавь эту строку

    queryset = Post.objects.all()
    lookup_field = 'slug'

    def list(self, request: DRFRequest) -> DRFResponse:
        """GET posts"""

        posts = Post.objects.filter(status='published').select_related("author").annotate(
            comments_count=Count("comments")
        )

        serializer = PostListSerializer(posts, many=True)
        return DRFResponse(data=serializer.data, status=HTTP_200_OK)

    def create(self, request: DRFRequest) -> DRFResponse:
        """POST Posts"""
        if not request.user.is_authenticated:
            return DRFResponse(status=401)

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return DRFResponse(data=serializer.data, status=HTTP_201_CREATED)

        return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """GET Slug"""
        post = get_object_or_404(Post, slug=slug)
        serializer = PostListSerializer(post)
        return DRFResponse(data=serializer.data, status=HTTP_200_OK)

    def partial_update(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """PATCH Slug"""
        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            return DRFResponse(
                data={"detail": "Вы не являетесь автором этого поста."},
                status=HTTP_403_FORBIDDEN
            )

        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return DRFResponse(data=serializer.data, status=HTTP_200_OK)

        return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """DELETE slug"""
        post = get_object_or_404(Post, slug=slug)

        if post.author != request.user:
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        post.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        """
        GET comments
        POST comments
        """
        post = get_object_or_404(Post, slug=slug)

        if request.method == 'GET':
            comments = post.comments.select_related("author").all()
            serializer = CommentSerializer(comments, many=True)
            return DRFResponse(data=serializer.data, status=HTTP_200_OK)

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return DRFResponse(status=401)

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return DRFResponse(data=serializer.data, status=HTTP_201_CREATED)

            return DRFResponse(data=serializer.errors, status=HTTP_400_BAD_REQUEST)