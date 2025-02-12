from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    employees = models.ManyToManyField(Employee)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title


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
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Task {self.task.title}"