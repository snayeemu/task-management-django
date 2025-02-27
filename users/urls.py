from django.contrib import admin
from django.urls import path
from users import views


urlpatterns = [
    path("create-user/", views.sign_up, name="create-user"),
    path("login/", views.sign_in, name="sign-in"),
    path("logout/", views.sign_out, name="sign-out"),
]
