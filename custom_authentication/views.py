
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth import authenticate , login  as dj_login , logout as dj_logout , update_session_auth_hash
from .forms import SignUpForm , loginForm
from django.contrib import messages

from .models import PlayerProfileModel
from .forms import PlayerProfileForm , UserChangePasswordForm , UpdateUserForm

from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , PasswordChangeForm , PasswordResetForm


from django.contrib.auth.models import User
import json
import requests




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










def login(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			fm = loginForm(request = request , data = request.POST)
			print(fm)
			if fm.is_valid():
				username = fm.cleaned_data["username"]
				password = fm.cleaned_data["password"]
				user = authenticate(username = username , password = password)
				if user is not None:
					dj_login(request  , user)
					print("Login Successfull ")
					return redirect("user_dashboard")
				else:
					print("Sorry User is not authenticated.")
					messages.error(request, "Either your email or password is wrong!")
			else:
				print("login Form data is not valid. ")
				context["form"]  = fm
		else:
			fm = loginForm()
		context = {
			"form" : fm
		}
		return render(request=request , template_name = 'custom_authentication/login.html' , context = context)
	return redirect("home")


	



def logout(request):
	if request.user.is_authenticated:
		print()
		dj_logout(request= request)
		if User.objects.filter(pk = request.user.id ):
			users = User.objects.filter(pk = request.user.id )
			if UserLoginSession.objects.filter(users = users):
				print("UserLoginSession Found")
				sessionkeys = UserLoginSession.objects.filter(users = users)
				for sk in sessionkeys:
					print(" sessionkeys Loop ")
					if Session.objects.filter(session_key=sk.session_key_id):							
						Session.objects.get(session_key=sk.session_key_id).delete()
						print("Session Deleted")
				else:
					if sessionkeys:
						print(" UserLoginSession after loop ")
						sessionkeys = UserLoginSession.objects.filter(users = users).delete()
						print(" UserLoginSession after loop Deleted ")





		return redirect("login")
	else:
		return redirect("login")








def user_profile(request):
	context = {}
	if request.user.is_authenticated:
		if PlayerProfileModel.objects.filter(users = request.user):
			player = PlayerProfileModel.objects.filter(users = request.user)
			context["player"] = player
			context["add_button"]  =  False
		else:
			context["player"]  = []
			context["add_button"]  =  True

	return render(request=request , template_name = 'userdashboard/user_profile.html' , context = context)



def update_profile(request):
	context = {}
	if request.user.is_authenticated:
		if PlayerProfileModel.objects.filter(users = request.user):
			if request.method == 'POST':
				player = PlayerProfileModel.objects.get(users = request.user)
				form = PlayerProfileForm(request.POST or None, instance=request.user)
				if form.is_valid():
					cnic_name = form.cleaned_data['cnic_name']
					nic = form.cleaned_data['nic']
					mobile = form.cleaned_data['mobile']
					country = form.cleaned_data['country']
					state = form.cleaned_data['state']
					city = form.cleaned_data['city']
					address = form.cleaned_data['address']
					PlayerProfileModel.objects.filter(users = request.user).update(
						cnic_name = cnic_name , nic=nic , mobile = mobile , country = country ,  state = state , city = city  , address = address )


					messages.success(request , " Update Successfully")
					# context["form"] = form
					return redirect('user_profile')
				else:
					print("Sorry data is not valid. ")
					context["form"]  = form
					messages.error(request , "Sorry Form Data is Not Valid. ")
			else:
				print("Get")
				player = PlayerProfileModel.objects.get(users = request.user)
				form = PlayerProfileForm(instance=player)
				context["form"]  = form
				picture_url = PlayerProfileModel.objects.get(users = request.user)
				if picture_url:
					context["picture_url"]  = picture_url
				else:
					context["picture_url"]  = {}



		else:
			context["player"]  = []
			context["add_button"]  =  True

	return render(request=request , template_name = 'userdashboard/update_profile.html' , context = context)











def add_profile(request):
	context = {}
	if request.user.is_authenticated:
		if request.POST:
			print("Request Is Post ")
			form = PlayerProfileForm(request.POST  , request.FILES )
			form.instance.users = request.user
			if form.is_valid():
				form.save()
				messages.success(request , " Created Successfully")
			else:
				print("Sorry data is not valid. ")
				messages.error(request , "Sorry Form Data is Not Valid. ")
		else:
			print("Request is get ")
			form = PlayerProfileForm()
			context = {
				"form" : form
			}
	return render(request=request , template_name = 'userdashboard/add_profile.html' , context = context)







def change_password(request):
	if request.method == 'POST':
		form = UserChangePasswordForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, ('Your password was successfully updated!'))
			return redirect('user_profile')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		form = UserChangePasswordForm(request.user)
	return render(request, 'custom_authentication/user_changed_password.html', {'form': form})






def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					msg_html = render_to_string('custom_authentication/password_reset_email.html',
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
							{"email_address": {"address": "waliullahthebo@gmail.com",
						"name":"quiztainment"}
						}],
						"subject":"Changed Password Request From Quiztainment",
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
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="custom_authentication/reset_password.html", context={"password_reset_form":password_reset_form})




def UpdateUser(request):
	if request.method == 'POST':
		context = {}
		form = UpdateUserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
   
			mobile = form.cleaned_data.get("phone")
			nic = form.cleaned_data.get("nic")
			cnic_name = form.cleaned_data.get("first_name")
   
			PlayerProfileModel.objects.filter(users = request.user).update(mobile = mobile,nic=nic,cnic_name=cnic_name)
			return redirect("user_profile")
		else:
			print("Form is not valid.")
			context = {
				"form" : form
			}


	else:
		form = UpdateUserForm(instance=request.user)
		context = {
			"form" : form
		}
	return render(request=request , template_name = 'userdashboard/update_user.html' , context = context)

