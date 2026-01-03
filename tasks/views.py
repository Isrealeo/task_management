from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer, CategorySerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Task Management!</h1>")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Owner + shared tasks
        queryset = Task.objects.filter(
            Q(owner=self.request.user) | Q(shared_with=self.request.user)
        ).distinct()

        # Query params
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        category = self.request.query_params.get("category")
        ordering = self.request.query_params.get("ordering")

        if status:
            status = status.upper()
            if status in ["PENDING", "COMPLETED"]:
                queryset = queryset.filter(status=status)

        if priority:
            priority = priority.capitalize()
            valid_priorities = [choice[0] for choice in Task.PRIORITY_CHOICES]
            if priority in valid_priorities:
                queryset = queryset.filter(priority=priority)

        if category:
            queryset = queryset.filter(category__name__iexact=category)

        if ordering in ["due_date", "-due_date", "priority", "-priority"]:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        task = self.get_object()
        if task.status == "COMPLETED":
            raise PermissionDenied("Completed tasks cannot be edited.")
        serializer.save()

    @action(detail=True, methods=["patch"])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = "COMPLETED"
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def revert(self, request, pk=None):
        task = self.get_object()
        task.status = "PENDING"
        task.completed_at = None
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
