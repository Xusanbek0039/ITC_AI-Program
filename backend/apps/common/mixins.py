from django.utils import timezone


class TimestampMixin:
    """Mixin to add created_at and updated_at to serializers."""
    pass


class OwnerQuerySetMixin:
    """Filter queryset by the requesting user."""

    owner_field = 'user'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field: self.request.user})
