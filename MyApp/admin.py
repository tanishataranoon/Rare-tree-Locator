from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# Register your models here.




# Customizing the UserAdmin to show user_type and profession
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("user_type", "profession")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("user_type", "profession")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "user_type", "profession", "is_staff")


# Simple ProfileAdmin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profession")
# unregister default if it exists
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# register the customized User model and Profile model
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)

