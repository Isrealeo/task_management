from rest_framework import serializers
from .models import Task, Category
from datetime import date
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Task
        fields = [
            "id", "owner", "title", "description", "status", "priority",
            "due_date", "completed_at", "created_at", "updated_at",
            "category", "recurrence", "shared_with"
        ]
        read_only_fields = ["owner", "completed_at", "created_at", "updated_at"]

    # ✅ Future due date validation
    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
