from django.contrib import admin

# Register your models here.
from django.contrib import admin
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel
from quizstart.models import QuizstartModel
from quizwinner.models import QuizwinnerModel , QuizwinnerAnnoucementModel




# Register your models here.
@admin.register(QuizwinnerModel)
class QuizwinnerAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('users' , 'quizopen' , 'quizresult' )
	exclude = ('creation' ,  )


# Register your models here.
@admin.register(QuizwinnerAnnoucementModel)
class QuizwinnerAnnouceAdmin(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('quizopen' ,  )
	exclude = ('creation' ,  )



