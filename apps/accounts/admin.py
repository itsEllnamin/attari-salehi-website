from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import UserCreationForm, UserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = ('mobile_number', 'email', 'name', 'family', 'is_active')
    ordering = ('mobile_number',)
    search_fields = ("mobile_number", "name", "family", "email")
    list_editable = ('is_active',)

    fieldsets = (
        ('اطلاعات ضروری', {'fields':('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields':('email', 'name', 'family')}),
        ('دسترسی‌ها', {'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {'fields':('mobile_number', 'email', 'name', 'family', 'password1', 'password2'),}),
    )