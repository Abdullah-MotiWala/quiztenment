from django.contrib import admin

# Register your models here.
from django.contrib import admin
from qestions.models import QuestionModel
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from import_export import resources

from  embed_video.admin  import  AdminVideoMixin
from .models  import  BannerVideo , Contact



# # Register your models here.
# @admin.register(QuestionModel)
# class QestionsAdmin(admin.ModelAdmin):
# 	'''Admin View for '''
# 	list_display = ('id' , 'question' , 'option_one' , 'option_two' , 'option_three' , 'option_four' , 'option_correct' , 'creation')
# 	# exclude = ('creation' ,  )

	


class QuestionResource(ImportExportModelAdmin, admin.ModelAdmin):
	class Meta:
		model = QuestionModel



class QuestionResource(resources.ModelResource):
	class Meta:
		model = QuestionModel
		# list_display = ('id' , 'question' , 'option_one' , 'option_two' , 'option_three' , 'option_four' , 'option_correct' , 'creation')


class QestionsAdmin(ImportExportModelAdmin):
	resource_class = QuestionResource
	list_display = ('id' , 'question' , 'option_one' , 'option_two' , 'option_three' , 'option_four' , 'option_correct' , 'creation')

admin.site.register(QuestionModel,QestionsAdmin)





# Register your models here.
@admin.register(BannerVideo)
class BannerVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('id' , 'banner_video' )
	# exclude = ('creation' ,  )



# Register your models here.
@admin.register(Contact)
class Contact(admin.ModelAdmin):
	'''Admin View for '''
	list_display = ('id' , 'name' , 'email' , 'phone' , 'subject' , 'message' , 'creation' )
	# exclude = ('creation' ,  )


