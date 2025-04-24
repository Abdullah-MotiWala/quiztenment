from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from  embed_video.fields  import  EmbedVideoField
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from django.urls import reverse

OPTIONS_CORRECT = (
	('1','1'),
	('2','2'),
	('3','3'),
	('4','4'),
)


class QuestionModel(models.Model):
	question = models.CharField(max_length=1055, null=True, blank=True)
	option_one = models.CharField(max_length=1055, null=True, blank=True)
	option_two = models.CharField(max_length=1055, null=True, blank=True)
	option_three = models.CharField(max_length=1055, null=True, blank=True)
	option_four = models.CharField(max_length=1055, null=True, blank=True)
	option_correct = models.CharField(max_length=6, choices=OPTIONS_CORRECT, default='2')
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.id)



#Create your models here.
class BannerVideo(models.Model):
	banner_video = EmbedVideoField()
	def  __str__(self):
		return  str(self.banner_video) 




class Contact(models.Model):
	name = models.CharField(max_length=1055, null=True, blank=True)
	email = models.CharField(max_length=1055, null=True, blank=True)
	phone = models.CharField(max_length=1055, null=True, blank=True)
	subject = models.CharField(max_length=1055, null=True, blank=True)
	message = models.CharField(max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)





	def __str__(self):
		return str( self.name)

