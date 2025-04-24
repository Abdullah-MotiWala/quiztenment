from django.contrib import admin

# Register your models here.
from django.contrib import admin
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel
from quizstart.models import QuizstartModel



from import_export.admin import ImportExportModelAdmin
from import_export import resources






class QuizstartResource(ImportExportModelAdmin, admin.ModelAdmin):
	class Meta:
		model = QuizstartModel



class QuizstartResource(resources.ModelResource):
	class Meta:
		model = QuizstartModel
		# list_display = ('id' ,  'quizstart'   , 'quizopen' ,  'status' , 'payment_game_status'  )
		fields = ('id'    , 'users__username' , 'quizopen__quiz_name' ,   'payment_status'  , 'payment_game_status' ,  'user_quiz_start_time' , 'user_quiz_end_time'  ,'ip_address' ,      'creation'  )

class QuizstartAdmin(ImportExportModelAdmin):
	resource_class = QuizstartResource
	list_display = ('id'    , 'users_id' , 'quizopen' ,   'payment_status'  , 'payment_game_status' ,  'user_quiz_start_time' , 'user_quiz_end_time'  ,'ip_address'    ,   'creation'   )


admin.site.register(QuizstartModel,QuizstartAdmin)






# Register your models here.
# @admin.register(QuizstartModel)
# class QuizstartAdmin(admin.ModelAdmin):
# 	'''Admin View for '''
# 	list_display = ('id' , 'users' , 'quizopen' , 'ip_address' , 'user_quiz_start_time' , 'user_quiz_end_time' , 'creation' )



