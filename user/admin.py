from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import UserCreationForm, UserChangeForm
from .models import User


# Register your models here.

class UsersAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    model = User

    list_display = ('email', 'is_admin', 'last_name', 'hire_date')

    list_filter = ('email', 'is_admin', 'last_name', 'hire_date')

    fieldsets = [('Details', {'fields': ('email', 'password', 'last_name', 'first_name',)}),
                 ('Info', {'fields': ('photo', 'about_me', 'phone', 'hire_date')}),
                 ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin', 'is_superuser')}), ]

    add_fieldsets = [('Details', {'fields': ('email', 'password1','password2', 'last_name', 'first_name',)}),
                     ('Info', {'fields': ('photo', 'about_me', 'phone', 'hire_date')}),
                     ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin', 'is_superuser')}), ]

    search_fields = ('email',)

    ordering = ('-hire_date',)


admin.site.register(User, UsersAdmin)
