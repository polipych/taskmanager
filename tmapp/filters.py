from django_filters import rest_framework as dj_filters
from .models import Task


class TaskFilterSet(dj_filters.FilterSet):
    """Набор фильров для представления для модели задач."""

    title = dj_filters.CharFilter(field_name="title", lookup_expr="icontains")
    # is_active = dj_filters.BooleanFilter(field_name="status", exclude=True)

    order_by_field = "ordering"

    class Meta:
        model = Task
        fields = [
            "title",
            "state",
        ]
