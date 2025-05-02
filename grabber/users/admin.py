from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'phone_number', "date_joined", "location", "password",'role')
    search_fields = ('email', 'first_name', 'last_name')

# Register your models here.
