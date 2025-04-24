from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.mail import BadHeaderError, send_mail , EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from django.utils.translation import gettext_lazy as _
from django_richtexteditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



# Create your models here.


class BlogPostModel(models.Model):
	title = models.CharField(max_length=1055, null=True, blank=True)
	meta_title = models.CharField(max_length=1055 , blank=True ,  null=True ,  default = 'title')
	meta_description = models.CharField(max_length=1055 , blank=True ,  null=True , default = 'description')

	msg = RichTextUploadingField(blank=True ,  null=True)
	pic = models.ImageField(upload_to='blog/')
	slug = models.SlugField(max_length=100 , unique=True)
	creation = models.DateTimeField(default=now, editable=False)
	date_updated = models.DateTimeField(_('date updated'), auto_now=True)



	class Meta:
		verbose_name=_('post')
		verbose_name_plural=_('posts')
		# ordering = ('-creation',)



	def __str__(self):
		return self.title


