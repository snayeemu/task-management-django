from django.urls import path
from tasks.views import (
    dashboard,
    user_dashboard,
    test,
    create_task,
    view_tasks,
    update_task,
    delete_task,
)

urlpatterns = [
    path("manager-dashboard/", dashboard, name="manager-dashboard"),
    path("user-dashboard/", user_dashboard),
    path("test/", test),
    path("create-task/", create_task, name="create-task"),
    path("view-tasks/", view_tasks),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
]
