from atexit import register
from django.contrib import admin
from .models import BlogPostModel

# Register your models here.
@admin.register(BlogPostModel)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title',     'msg' ,  'meta_title' , 'meta_description' ,   'creation' , 'date_updated' ]


