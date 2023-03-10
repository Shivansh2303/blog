from django.contrib import admin
from .models import UserModel
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


class UserAdminConfig(UserAdmin):
    search_fields=('email','user_name')
    list_filter=('email','user_name','is_active','is_staff')
    ordering=('-start_date',)
    list_display=('email','user_name','is_active','is_staff')
    
    fieldsets=(
        (None,{'fields':('email','user_name',)}),
        ('Permissions',{'fields':('is_staff','is_active')}),
    
    )
        
   
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','user_name','password'), 
        })
    )
      
admin.site.register(UserModel)