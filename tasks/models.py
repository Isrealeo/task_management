from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
    ]
    RECURRENCE_CHOICES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Stretch goal fields
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, null=True, blank=True)
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_tasks")
    reminder_sent = models.BooleanField(default=False)  # for notifications

    def __str__(self):
        return self.title
