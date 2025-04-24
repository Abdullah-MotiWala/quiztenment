from django.contrib import admin

# Register your models here.
from django.contrib import admin
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel
from quizstart.models import QuizstartModel
from quizpayment.models import QuizpaymentModel  , QuizpaymentResponseAPI

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import QuizpaymentModel










class QuizpaymentResource(ImportExportModelAdmin, admin.ModelAdmin):
	class Meta:
		model = QuizpaymentModel



class QuizpaymentResource(resources.ModelResource):
	class Meta:
		model = QuizpaymentModel
		# list_display = ('id' ,  'quizstart'   , 'quizopen' ,  'status' , 'payment_game_status'  )


class QuizpaymentAdmin(ImportExportModelAdmin):
	resource_class = QuizpaymentResource
	list_display = ('id' ,  'quizstart'   , 'quizopen' ,  'status' , 'payment_game_status'  )
	exclude = ('creation' ,  )


admin.site.register(QuizpaymentModel,QuizpaymentAdmin)






# Register your models here.
# @admin.register(QuizpaymentModel)
# class QuizpaymentAdmin(admin.ModelAdmin):
# 	'''Admin View for '''
# 	list_display = ('id' ,  'quizstart'   , 'quizopen' ,  'status' , 'payment_game_status'  )
# 	exclude = ('creation' ,  )



# Register your models here.
@admin.register(QuizpaymentResponseAPI)
class QuizpaymentResponseAPI(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('id' ,  'query_params'   , 'creation' ,    )

