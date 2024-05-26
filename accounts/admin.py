from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Profile, Skill, University, Gender,Follow,SubSkill,UserMainSkill,UserSubSkill



class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)  # Display users ordered by email instead of username


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(University)
admin.site.register(Gender)
admin.site.register(Follow)
admin.site.register(SubSkill)
admin.site.register(UserMainSkill)
admin.site.register(UserSubSkill)
