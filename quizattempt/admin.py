from django.db import models
from .models import QuizattemptModel
from django.contrib import admin


# Register your models here.
@admin.register(QuizattemptModel)
class QuizattemptAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('id' , 'assignedquiz' , 'submitted_answer' , 'compared_answer' ,  'status' , 'ip_address')
	exclude = ('creation' ,  )


