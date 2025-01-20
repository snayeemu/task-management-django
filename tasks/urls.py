from django.urls import path
from tasks.views import dashboard, user_dashboard, test

urlpatterns = [
    path('manager-dashboard/', dashboard),
    path('user-dashboard/', user_dashboard),
    path('test/', test)
]