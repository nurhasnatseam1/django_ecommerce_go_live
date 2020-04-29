from django.contrib import admin
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import Group 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

from .models import GuestEmail 
from .forms import UserAdminCreationForm,UserAdminChangeForm
User=get_user_model() #gives you the current User model , that one you setted up in settngs.py

 
class UserAdmin(BaseUserAdmin):
      form=UserAdminChangeForm 
      add_form=UserAdminCreationForm 

      list_display=('email','admin','staff') #which fields would be represented in list columns
      list_filter=('admin',) #filter the list of users by this fields

      #what this fieldsets are doing is using them we are redefining and restructuring the adminModelForms declared above
      fieldsets=(
            (None,{"fields":('email','password')}),
            ("Personal info",{'fields':('full_name',)}),
            ("Permissions",{'fields':('admin','is_adim')}),

      )
      add_fieldsets=(
            (None,{'classes':('wide',),
            'fields':('email','password1','password2')}
            ),
      )
      search_fields=['email']
      ordering=('email',)
      filter_horizontal=()#i have no idea what this does 

admin.site.register(User,UserAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
      class Meta:
            model=GuestEmail

admin.site.register(GuestEmail,GuestEmailAdmin)


admin.site.unregister(Group)
