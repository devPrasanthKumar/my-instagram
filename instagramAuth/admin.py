from django.contrib import admin

# Register your models here.
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "phone_number"]


admin.site.register(CustomUser, CustomUserAdmin)
