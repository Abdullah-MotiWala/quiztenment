from django.db import models
from datetime import timedelta
from django.utils.timezone import utc

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime
from django.urls import reverse

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from smtplib import SMTPException
import requests
import json
import time

QUIZOPEN_STATUS = (
	('CLOSED','CLOSED'),
	('CANCELLED','CANCELLED'),
	('OPENED','OPENED'),
)




class QuizopenModel(models.Model):
	# users = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz_name = models.CharField(max_length=1055, null=True, blank=True)
	price_name = models.CharField(max_length=1055, null=True, blank=True)
	quiz_numbers = models.IntegerField( null=True, blank=True)
	quiz_payment = models.IntegerField( null=True, blank=True , default = '1')
	start_date_time = models.DateTimeField( null=True, blank=True)
	end_date_time = models.DateTimeField(null=True, blank=True)
	duation_time = models.DurationField( default=timedelta(minutes=30) ,  null=True, blank=True)
	status = models.CharField(max_length=100, choices=QUIZOPEN_STATUS, default='OPENED')
	send_email_request = models.BooleanField(default = False)

	creation = models.DateTimeField(default=now, editable=False )
 
	def save(self, *args, **kwargs):
		super(QuizopenModel, self).save(*args, **kwargs)
		if self.status == 'OPENED' and self.send_email_request:
			user_list = User.objects.all()
			msg_html = render_to_string('custom_authentication/open_quiz_email_template.html',
			{
				'quiz_name': self.quiz_name,
				'quiz_payment': self.quiz_payment,
				'quiz_numbers': self.quiz_numbers,
				'start_date_time': self.start_date_time,
				'end_date_time': self.end_date_time,
				'duation_time': self.duation_time,
			}) 
			for i in user_list:
				if i.email:
					url = "https://api.zeptomail.com/v1.1/email"
					payload = {
						'bounce_address':"bounce1@bounce.quiztainment.com.pk",
						"from": {"address": "noreply@quiztainment.com.pk"},
						"to": [
							{"email_address": {"address": "{}".format(i.email),
						"name":"quiztainment"}
						}],
						"subject":"Test Email",
						"htmlbody":  "{}".format(msg_html)
						}
					headers = {
					'accept': "application/json",
					'content-type': "application/json",
					'authorization': "Zoho-enczapikey wSsVR61yrBGlD6p1mGKsc+c4ywhTB1KlFEV6igej73L0SPjDp8c/whfLAgXzHfdMFGVtFmZAoe98mhgI0DIKj9l8zQtWCSiF9mqRe1U4J3x17qnvhDzIWWlfkBSLJYMBxwltnGFjE8or+g==",
					}
					try:
						response = requests.request("POST", url, data=json.dumps(payload), headers=headers)						
					except requests.exceptions.HTTPError as errh:
						print ("Http Error:",errh)
					except requests.exceptions.ConnectionError as errc:
						print ("Error Connecting:",errc)
					except requests.exceptions.Timeout as errt:
						print ("Timeout Error:",errt)
					except requests.exceptions.RequestException as err:
						print ("OOps: Something Else",err)
				time.sleep(10)









	def __str__(self):
		return str( self.quiz_name)


	def now_diff(self):
		delta = datetime.now() - self.end_date_time
		return delta.total_seconds() / (60 * 60)



	def get_time_diff(self):
		if self.end_date_time:
			now = datetime.datetime.utcnow().replace(tzinfo=utc)
			timediff = self.end_date_time - now
			return timediff
			return timediff.total_seconds()


	class Meta:
		ordering = ['-creation']