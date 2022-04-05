from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (
    ('Nickname fields', {'fields': ('nickname', )}),
    ('Address fields', {'fields': ('address', )}),
    ('lat fields', {'fields': ('lat', )}),
    ('lon fields', {'fields': ('lon', )}),
) 