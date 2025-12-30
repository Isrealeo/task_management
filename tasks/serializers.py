from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import date
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
        def create(self, validated_data):
            user = User(
                username = validated_data ['username'],
                email = validated_data ['email'],
            )
            user.set_password(validated_data ['password'])
            user.save()
            return user

    
class TaskSerializer(serializers.ModelSerializer):

    priority = serializers.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        default="medium"
    )

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Due date must be in the future."
            )
        return value

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "owner",
            "completed_at",
            "created_at",
            "updated_at",
        )
