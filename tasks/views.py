from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Start with tasks belonging to the logged-in user
        queryset = Task.objects.filter(owner=self.request.user)

         # Get query parameters
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        ordering = self.request.query_params.get("ordering")

            # Filter by status (ensure uppercase match)
        if status:
            status = status.upper()
            if status in ["PENDING", "COMPLETED"]:
                queryset = queryset.filter(status=status)

         # Filter by priority (normalize to match model values)
        if priority:
            priority = priority.capitalize()  # "low" -> "Low"
            valid_priorities = [choice[0] for choice in Task.PRIORITY_CHOICES]
            if priority in valid_priorities:
                queryset = queryset.filter(priority=priority)
    # Ordering
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
    def revert(self, request, pk=None):
        task = self.get_object()
        task.status = "PENDING"
        task.completed_at = None
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

