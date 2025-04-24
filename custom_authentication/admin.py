from django.db import models
from .models import PlayerProfileModel
from django.contrib import admin


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin

from import_export import resources
from django.contrib import admin







class UserResource(resources.ModelResource):
	class Meta:
		model = User
		fields = ('id' , 'first_name', 'last_name', 'email' , 'date_joined')

class UserAdmin(BaseAdmin, ImportExportModelAdmin):
	resource_class = UserResource



admin.site.unregister(User)
admin.site.register(User, UserAdmin)









# Register your models here.
@admin.register(PlayerProfileModel)
class PlayerProfileAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('users' , 'cnic_name', 'nic'  ,  'mobile' , 'country' , 'state' , 'city' , 'address'  , )
	exclude = ('creation' ,  )


