from django.urls import path
from tasks.views import (
    manager_dashboard,
    employee_dashboard,
    create_task,
    view_tasks,
    update_task,
    task_details,
    delete_task,
)

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("employee-dashboard/", employee_dashboard, name="employee-dashboard"),
    path("create-task/", create_task, name="create-task"),
    path("view-tasks/", view_tasks, name="view-tasks"),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("task/<int:id>/details/", task_details, name="task-details"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
]
