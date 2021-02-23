from django.contrib import admin
from .models import CustomUser, Reminders
from django.contrib.auth.models import Group

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Reminders)
admin.site.unregister(Group)