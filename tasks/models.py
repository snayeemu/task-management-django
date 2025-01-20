from django.db import models

# Create your models here.
class Tasks(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskDetails(models.Model):
    task = models.OneToOneField(Tasks, on_delete=models.CASCADE)
    high = "h"
    medium = "m"
    low = "l"
    priority_options = {
        high: "high",
        medium: "medium",
        low: "low",
    }
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=priority_options, default=low)