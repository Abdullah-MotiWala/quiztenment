from django.contrib import admin

# Register your models here.
from django.contrib import admin
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel

from import_export.admin import ImportExportModelAdmin

from import_export import resources





# # Register your models here.
# @admin.register(QuizresultModel)
# class QuizresultAdmin(admin.ModelAdmin):

# 	'''Admin View for '''
# 	list_display = ('id','users' , 'quizopen' , 'user_time_duration' , 'corrent_anwswer' , 
# 	'skipped_anwswer' ,
# 	'total_attempt_answer' , 'total_assigned_answer' ,  'total_submitted_answer'
# 	, 'percantage' , 'final_score')
# 	exclude = ('creation' ,  )
# 	order_by = ('final_score', )



class QuizresultResource(ImportExportModelAdmin, admin.ModelAdmin):
	class Meta:
		model = QuizresultModel
		order_by = ('-awnsers_percantage', )


class QuizresultResource(resources.ModelResource):
	class Meta:
		model = QuizresultModel
		# list_display = ('id' , 'question' , 'option_one' , 'option_two' , 'option_three' , 'option_four' , 'option_correct' , 'creation')


class QuizresultAdmin(ImportExportModelAdmin):
	resource_class = QuizresultResource

	'''Admin View for '''
	list_display = ('id','users' , 'quizopen' , 'user_time_duration' , 'user_time_duration_actual' ,  'corrent_anwswer' , 
	'skipped_anwswer' ,
	'total_attempt_answer' , 'total_assigned_answer' ,  'total_submitted_answer'
	, 'percantage' , 'final_score' , 'marit_status' , 'awnsers_percantage' , 'creation' )
	# exclude = ('creation' ,  )
	order_by = ('-awnsers_percantage', )


admin.site.register(QuizresultModel,QuizresultAdmin)



