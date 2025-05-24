from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'gender',
        'first_name',
        'last_name',
        'phone',
        'email',
        'location',
        'picture',
    )
