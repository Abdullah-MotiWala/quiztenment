from email import message
from tkinter import Widget
from typing_extensions import Required
from django.db import models

from django import forms 
from django_countries.fields import CountryField

from django_countries.data import COUNTRIES
from django_countries.widgets import CountrySelectWidget
from datetime import datetime
from django.utils.timezone import now


from custom_blog.models import BlogPostModel

from django.contrib.auth.models import User

# class POSTForm(forms.ModelForm):
# 	# content = forms.CharField(widget=CKEditorWidget())
#   	content = forms.CharField(widget=forms.Textarea)
# 	def __init__(self, *args, **kwargs):
# 		super(POSTForm,self).__init__(*args, **kwargs)
# 		if self.instance.pk is None: # form is new
# 			print(" Form is new ")
# 		else:
# 			print(" Form is For Updated ")


# 	class Meta:
# 		model = BlogPostModel
# 		fields = ['title',  'content' , 'creation' ]
# 		widgets = {
# 		'title': forms.TextInput(attrs={'class': 'form-control'  }),
# 		'content': forms.Textarea(attrs={'class': 'form-control' , 'rows': 6 , 'cols': 80 }),
# 		}
		
# 	def clean_title(self):
# 		if self.instance.pk is None:
# 			print("Form is New ")
# 		else:
# 			print(" Form is for update. ")







