from django.db import models
from .models import AssignedquizModel
from django.contrib import admin


# Register your models here.
@admin.register(AssignedquizModel)
class AssignedquizAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('id' , 'quizstart' , 'users' , 'quizopen' , 'question' , 'correct_answer' ,'ip_address', 'creation')
	# exclude = ('creation' ,  )


