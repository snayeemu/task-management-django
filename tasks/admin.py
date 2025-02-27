from django.contrib import admin
from tasks import models 

admin.site.register(models.Employee)
admin.site.register(models.Project)
admin.site.register(models.TaskDetails)
admin.site.register(models.Tasks)

# Register your models here.
