from django.contrib import admin
from django.urls import path
from users import views


urlpatterns = [
    path("sign-up/", views.sign_up, name="sign-up"),
    path("login/", views.sign_in, name="sign-in"),
    path("logout/", views.sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", views.activate_user),
    path("admin/dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path("admin/assign-role/<int:user_id>/", views.assign_role, name="assign-role"),
    path("admin/create-group/", views.create_group, name="create-group"),
    path("admin/group-list/", views.group_list, name="group-list"),
]
