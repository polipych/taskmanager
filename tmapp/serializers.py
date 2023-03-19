from rest_framework import serializers
from tmapp.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор по модели Task."""

    class Meta:
        model = Task
        read_only_fields = ["id", "task_start"]
        fields = read_only_fields + [
            "title",
            "keyid",
            "project",
            "author",
            "sprint",
            "state",
            "task_update",
            "executor",
        ]

        # fields = "__all__"
