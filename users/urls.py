from django.contrib import admin
from django.urls import path
from users import views


urlpatterns = [
    path("sign-up/", views.sign_up, name="sign-up"),
    path("login/", views.sign_in, name="sign-in"),
    path("logout/", views.sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", views.activate_user),
]
