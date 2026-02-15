from django.db.models import (
    Model,
    DateTimeField,
)

class Abstact(Model):
    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )
    class Meta:
        abstract = True
