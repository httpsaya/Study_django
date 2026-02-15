# Python modules
from typing import Any
from settings.base import AUTH_USER_MODEL

# Django modules
import uuid
from django.db.models import (
    CharField,
    TextChoices,
    SlugField,
    ForeignKey,
    CASCADE,
    TextField,
    SET_NULL,
    ManyToManyField,
)
from apps.abstracts.models import Abstact
from django.utils import timezone
from datetime import timedelta

NAME_MAX_LENGTH = 50


class Tag(Abstact):

    name =  CharField(
        max_length=NAME_MAX_LENGTH
    )
    slug = SlugField(unique=True)


class Category(Abstact):
    name = CharField(
        max_length=NAME_MAX_LENGTH
    )
    slug = SlugField(
        unique=True
    )


class Post(Abstact):
    """Post model with common fields"""
    CATEGORY_MAX_LENGTH = 150
    TITLE_MAX_LENGTH = 200
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    STATUS_MAX_LENGTH=200
    author = ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=CASCADE
    )

    title = CharField(
        max_length=TITLE_MAX_LENGTH
    )

    slug = SlugField(unique=True)

    body = TextField()

    category = ForeignKey(
        to=Category,
        on_delete = SET_NULL,
        null=True,
        blank=True,
    )

    tags = ManyToManyField(
        to=Tag,
        blank=True,
    )

    status = CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default='draft',
    )


class Comment(Abstact):
    post = ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name='comments',
    )
    author = ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=CASCADE
    )

    body = TextField()
