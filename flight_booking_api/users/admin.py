from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

from .forms import AdminUserChangeForm

# Register your models here.
 

class UserAdmin(BaseUserAdmin):

    # Model to be used
    model = User

    # The forms to add and change user instances
    form = AdminUserChangeForm
    add_form = AdminUserChangeForm

    # The fields to be used in displaying the User Model
    list_display = ('id','first_name','last_name','email','is_admin',)
    list_filter = ('first_name', 'last_name','email',)

    fieldsets = (
        (None,{'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name', 'photo')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active','is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('phone','password', 'password2')
        }),
    )

    search_fields = ('email','first_name','last_name')
    ordering = ('email','first_name','last_name')
    filer_horizontal = ()

    def get_inline_instances(self,request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Register user model
admin.site.register(User, )

# Remove Group Model from Admin.
admin.site.unregister(Group, )
