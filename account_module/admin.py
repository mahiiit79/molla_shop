from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter = ['about_user']
admin.site.register(models.User)
