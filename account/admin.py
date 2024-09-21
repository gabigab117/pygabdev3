from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = SignUpForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = UserAdmin.fieldsets  # + ((None, {"fields": ["custom_field"]}),)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "last_name", "first_name", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "is_superuser"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
