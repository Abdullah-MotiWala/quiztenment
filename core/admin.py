from django.db import models
from .models import DummyDataDisplayModel , SendEmailAllUserModel , SendEmailAllUserPaidModel
from django.contrib import admin


# Register your models here.
@admin.register(DummyDataDisplayModel)
class DummyDataDisplayAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('choose_users' , 'user_satisfaction_rate', 'user_growth_rate'  ,  'next_segment' )
	exclude = ('creation' ,  )




# Register your models here.
@admin.register(SendEmailAllUserModel)
class SendEmailAllUserAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('start' , 'end' )
	exclude = ('creation' ,  )

# Register your models here.
@admin.register(SendEmailAllUserPaidModel)
class SendEmailAllUserPaidAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('start' , 'end' )
	exclude = ('creation' ,  )




