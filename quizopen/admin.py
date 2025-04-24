from django.contrib import admin

# Register your models here.
from django.contrib import admin
from quizopen.models import QuizopenModel

@admin.register(QuizopenModel)
class QuizopenAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display  = ('id' , 'quiz_name' , 'price_name' , 'quiz_numbers' , 'start_date_time' , 'end_date_time' 
	, 'status' , 'send_email_request' )
	exclude = ('creation' ,  )


