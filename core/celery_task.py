import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

import json
import requests

from quizpayment.models import QuizstartModel




from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from smtplib import SMTPException
from custom_authentication.models import UserLoginSession
from django.contrib.sessions.models import Session  








@shared_task
def create_random_user_accounts(total):
	print("created User ")
	for i in range(total):
		username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
		email = '{}@example.com'.format(username)
		password = get_random_string(50)
		User.objects.create_user(username=username, email=email, password=password)
	return '{} random users created with success!'.format (total)

@shared_task
def send_email_message_to_users():
	users = User.objects.all()
	for i in range(10):
		subject = 'Thank you for registering to our site'
		message = ' it  means a world to us '
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['waliullah.getsolution@gmail.com',]
		send_mail( subject, message, email_from, recipient_list )



@shared_task
def sending_email_all_user(start = 1 , end = 10):
	users = User.objects.all()[int(start):int(end)]
	for user in users:
		print(user)
		if user.email:
			print("sending_email_all_user")
			msg_html = render_to_string('custom_authentication/email_all_user_freeze.html',
			{
			"email":user.email,
			'domain':'quiztainment.com.pk',
			'site_name': 'Website',
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user.username,
			'token': default_token_generator.make_token(user),
			'protocol': 'https',
			}
			) 
			url = "https://api.zeptomail.com/v1.1/email"
			payload = {
				'bounce_address':"bounce1@bounce.quiztainment.com.pk",
				"from": {"address": "noreply@quiztainment.com.pk"},
				"to": [
					{"email_address": {"address": user.email,
				"name":"quiztainment"}
				}],
				"subject":"BREAKING NEWS",
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



@shared_task
def sending_email_all_user_paid(start = 1 , end = 10):
	print("sending_email_all_user_paid")
	users = QuizstartModel.objects.filter(payment_status = 'PAID').select_related('users').values_list('users_id' , 'users__username' , 'users__email').distinct()
	for i in users:
		if i[2] == "":
			print("Email is not found.")
		else:
			print("Please Send EMail")
			if i[2]:
				print("sending_email_all_user")
				msg_html = render_to_string('custom_authentication/email_all_paid_user_freeze.html',
				{
				"email":i[2],
				'domain':'quiztainment.com.pk',
				'site_name': 'Website',
				"user": i[1],
				}
				) 
				url = "https://api.zeptomail.com/v1.1/email"
				payload = {
					'bounce_address':"bounce1@bounce.quiztainment.com.pk",
					"from": {"address": "noreply@quiztainment.com.pk"},
					"to": [
						{"email_address": {"address": i[2],
					"name":"quiztainment"}
					}],
					"subject":"BREAKING NEWS",
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









