from django.contrib import admin
from .models import Task, PCS_Cloud

# Register your models here.
admin.site.register(PCS_Cloud)
admin.site.register(Task)