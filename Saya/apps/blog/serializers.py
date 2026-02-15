# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Field
)

# Project modules
from apps.blog.models import Post, Comment, Category, Tag
from apps.abstracts.serializers import CustomUserForeignSerializer

class PostBaseSerializer(ModelSerializer):
    """
    Base serializer for Post instances.
    """

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(PostBaseSerializer):
    """
    Serializer for listing Post instances with count of comments and author details.
    """

    author = CustomUserForeignSerializer(read_only=True)
    comments_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "status",
            "comments_count",
            "created_at",
        )

    def get_comments_count(self, obj: Post) -> int:
        """
        Get the count of comments associated with the post.
        """
        return getattr(obj, "comments_count", obj.comments.count())


class PostCreateSerializer(PostBaseSerializer):
    """
    Serializer for creating Post instances.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "category",
            "slug",
            "tags",
            "status",
        )


class PostUpdateSerializer(PostBaseSerializer):
    """
    Serializer for updating Post instances.
    """

    class Meta:
        model = Post
        fields = (
            "title",
            "category",
            "tags",
            "status",
        )


class CommentSerializer(ModelSerializer):
    """
    Serializer for Comment instances.
    """
    author = CustomUserForeignSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "body",
            "created_at",
        )
        read_only_fields = ("id", "post", "author", "created_at")