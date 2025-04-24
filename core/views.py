from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , PasswordChangeForm , PasswordResetForm
from django.contrib.auth import authenticate , login  as dj_login , logout as dj_logout , update_session_auth_hash
from  custom_authentication.forms import SignUpForm , loginForm
from custom_authentication.models import PlayerProfileModel
from django.contrib import messages
from quizpayment.models import QuizpaymentModel  , QuizpaymentItsModel , QuizpaymentResponseAPI
from quizpayment.models import QuizstartModel
from quizopen.models import QuizopenModel
from django.contrib.auth.models import User  
from qestions.models import QuestionModel
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import  QuizattemptModel
from quizresult.models import QuizresultModel
from custom_blog.models import BlogPostModel

from custom_authentication.models import UserLoginSession
from django.contrib.sessions.models import Session  


from django.db.models import Q
from django.db.models import Exists, OuterRef
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMessage

from django.views.decorators.csrf import csrf_exempt

from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from smtplib import SMTPException
import requests

from django import db


from datetime import datetime
from datetime import timedelta


from django.contrib import messages
import json

import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from  qestions.models  import  BannerVideo , Contact
from quizwinner.models import QuizwinnerModel
from quizstart.models import QuizstartModel
from core.models import DummyDataDisplayModel



# Create your views here.


def home(request):
	context = {}
	product_list = []

	user_count = User.objects.all().count()
	
	played_count = QuizstartModel.objects.all().count()
	winner_count = QuizwinnerModel.objects.all().count()

	
	dummy_data = DummyDataDisplayModel.objects.filter(pk = 1)
	if dummy_data:
		user_count = dummy_data[0].choose_users
	
	
	
	
	video  = BannerVideo.objects.filter(pk = 1)






	context = {
		"video" : video,
		"user_count" : user_count,
		"played_count" : played_count,
		"winner_count" : winner_count,
		'quiz_data' : get_detail_quiz(),

	}
	return render(request=request , template_name = 'core/index.html'  ,context= context )


def about(request):
	context = {}
	product_list = []
	context = {
		'quiz_data' : get_detail_quiz(),
	}

	return render(request=request , template_name = 'core/about.html'  ,context= context )


def r_404_view(request):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
   return render(request, 'core/404.html')

def error_404_view(request, exception=None):
   #return render(request, 'core/404.html')
   return HttpResponseRedirect("/404")


def marque(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/marque_top.html'  ,context= context )






def policy(request):
	context = {}
	product_list = []
	context = {
		'quiz_data' : get_detail_quiz(),
	}


	return render(request=request , template_name = 'core/policy.html'  ,context= context )


def terms(request):
	context = {}
	product_list = []
	context = {
		'quiz_data' : get_detail_quiz(),
	}

	return render(request=request , template_name = 'core/terms.html'  ,context= context )





def mini_blog(request):
	post = BlogPostModel.objects.all()
	records = []
	for i in post:
		row = {
			"id" : i.id , 
			"title" : i.title , 
			"slug" : i.slug , 
			"pic" : i.pic or "", 
			"meta_title" : i.meta_title or "", 
			"meta_description" : i.meta_description or "", 


			"creation" : i.creation , 
		}
		records.append(row)

	context = {
		'post' : records,
		'quiz_data' : get_detail_quiz(),

	}
	return render(request=request , template_name = 'core/mini_blog.html'  ,context= context )


def mini_blog_detail(request , slug):
	post = BlogPostModel.objects.filter(slug = slug)
	records = []
	for i in post:
		row = {
			"id" : i.id , 
			"title" : i.title , 
			"msg" : i.msg, 
			"meta_title" : i.meta_title or "", 
			"meta_description" : i.meta_description or "", 
			"pic" : i.pic or "", 
			"creation" : i.creation , 
		}
		records.append(row)

	context = {
		'post' : records,
		'quiz_data' : get_detail_quiz(),

	}
	return render(request=request , template_name = 'core/mini_blog_detail.html'  ,context= context )






def faq(request):
	context = {}
	product_list = []
	context = {
		'quiz_data' : get_detail_quiz(),
	}

	return render(request=request , template_name = 'core/faq.html'  ,context= context )




def score_board(request):
	user_result = []
	my_user_result = []

	# order_by('-check_in')

	result = QuizresultModel.objects.filter(awnsers_percantage__gte = 60 , new_status = 'NONFREE' ).order_by("-creation", "-corrent_anwswer", "user_time_duration_actual")[:20]
	if result:
		user_result  = result
	
	my_result = QuizresultModel.objects.filter(users_id = request.user.id ,  new_status = 'NONFREE').order_by("-creation", "-corrent_anwswer")[:11]
	if my_result:
		my_user_result  = my_result




	context = {
		"result" : user_result , 
		"my_result" : my_user_result,
		"today" : datetime.now().date(),
		'quiz_data' : get_detail_quiz(),


	}
	product_list = []
	return render(request=request , template_name = 'core/score_board.html'  ,context= context )




def free_score_board(request):
	user_result = []
	my_user_result = []

	# order_by('-check_in')

	result = QuizresultModel.objects.filter(awnsers_percantage__gte = 60 , new_status = 'FREE' ).order_by("-corrent_anwswer", "user_time_duration_actual") 
	if result:
		user_result  = result
	
	my_result = QuizresultModel.objects.filter(users_id = request.user.id ,  new_status = 'FREE').order_by("-corrent_anwswer") 
	if my_result:
		my_user_result  = my_result




	context = {
		"result" : user_result , 
		"my_result" : my_user_result,
 		"today" : datetime.now().date(),
        # "today" : datetime.date(2022, 12, 31),
        #   "today" : datetime.datetime(2022, 12, 31),
		'quiz_data' : get_detail_quiz(),


	}
	product_list = []
	return render(request=request , template_name = 'core/free_score_board.html'  ,context= context )




def contact(request):
	context = {}
	product_list = []
	if request.method== 'POST':
		first_name = request.POST.get("first_name")
		email = request.POST.get("email")
		phone = request.POST.get("phone")
		subject = request.POST.get("subject")
		business_text = request.POST.get("business_text")
		u = Contact.objects.create(name =first_name ,  email = email ,  phone = phone ,  message = business_text)
		u.save()
		messages.success(request, "Thankyou for contact us. ")
		if u.email:
			msg_html = render_to_string('custom_authentication/contact_template.html',
			{ 'first_name' : first_name  }
			) 
			url = "https://api.zeptomail.com/v1.1/email"
			payload = {
				'bounce_address':"bounce1@bounce.quiztainment.com.pk",
				"from": {"address": "noreply@quiztainment.com.pk"},
				"to": [
					{"email_address": {"address": email,
				"name":"quiztainment"}
				}],
				"subject":subject or "",
				"htmlbody":  "Thankyou For your Feedback | query: " or ""
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






	else:
		print("Request GET")
	context = {
		'quiz_data' : get_detail_quiz(),
	}

	return render(request=request , template_name = 'core/contact.html'  ,context= context )




def open_quiz_list(request):
	# quiz_open  = QuizopenModel.objects.filter()
	quiz_open = QuizopenModel.objects.filter(Q( end_date_time__gt= datetime.now() , status = 'OPENED'))

	context = {"quiz_open" : quiz_open}
	return render(request=request , template_name = 'core/index_open_quiz.html'  ,context= context )



# @csrf_exempt
# def login(request):
# 	if not request.user.is_authenticated:
# 		context = {}
# 		if request.method == 'POST':
# 			fm = loginForm(request = request , data = request.POST)
# 			print(fm)
# 			if fm.is_valid():
# 				username = fm.cleaned_data["username"]
# 				password = fm.cleaned_data["password"]
# 				user = authenticate(username = username , password = password)
# 				if user is not None:
# 					dj_login(request  , user)
# 					print("Login Successfull ")
# 					return redirect("user_dashboard")
# 				else:
# 					print("Sorry User is not authenticated.")
# 					messages.error(request, "Either your email or password is wrong!")
# 			else:
# 				print("login Form data is not valid. ")
# 				messages.error(request, "Either your email or password is wrong!")
# 				context["user_login_form"]  = fm

# 		else:
# 			fm = loginForm()
# 		context = {
# 			"user_login_form" : fm,
# 			'quiz_data' : get_detail_quiz(),

# 		}
# 		return render(request=request , template_name = 'core/login.html' , context = context)
# 	return redirect("user_dashboard")










# Login View Function
@csrf_exempt
def login(request):
	context = {}	
	if not request.user.is_authenticated:
		if request.method == "POST" and 'login' in request.POST:
			print("Request is POST with login ")
			fm = loginForm(data=request.POST or None)
			if fm.is_valid():
				uname = fm.cleaned_data['username']
				upass = fm.cleaned_data['password']
				user = authenticate(username=uname, password=upass)
				if user is not None:
					muser = User.objects.get(username = uname)
					print("muser" , muser)
					# if UserLoginSession.objects.filter(users = muser):
					# 	print(" UserLoginSession Found  ")
					# 	context["continue"] = True
					# 	fm = loginForm(data=request.POST or None)
					# 	context["user_id"] = user.id
					# 	context["uname"] = uname
					# 	context["user_login_password"] = upass
						# context["user_login_form"] = fm
					
						# messages.warning(request, 'BY LOGGING HERE YOU WILL BE LOGGED OUT FROM OTHER BROWSER')
					# else:
					print(" UserLoginSession User Not Foudn. ")
					dj_login(request, user)
					if request.session.session_key:
						key = request.session.session_key
						print("Login Session Key ")
						print(key)
						create_login_session_user(user , key)
						return redirect("user_dashboard")


			else:
				print("user is not validate ")
				context = {
					'user_login_form': fm , 
					'continue': False
				}
				messages.error(request, 'Login Detail is Wrong !!')
		
		if request.method == "POST" and 'continue' in request.POST:
			user_login_id = request.POST.get("user_login_id")
			uname = request.POST.get("uname")
			user_login_password = request.POST.get("user_login_password")
			print("Request is POST with continue " , user_login_id)	
			if uname and user_login_password:
				print("username and user_login_password ")
				user = authenticate(username=uname, password=user_login_password)
				if user is not None:
					if UserLoginSession.objects.filter(users = user):
						print("UserLoginSession Found")
						sessionkeys = UserLoginSession.objects.filter(users = user)
						for sk in sessionkeys:
							print(" sessionkeys Loop ")
							if Session.objects.filter(session_key=sk.session_key_id):							
								Session.objects.get(session_key=sk.session_key_id).delete()
								print("Session Deleted")
						else:
							if sessionkeys:
								print(" UserLoginSession after loop ")
								sessionkeys = UserLoginSession.objects.filter(users = user).delete()
								print(" UserLoginSession after loop Deleted ")

					dj_login(request, user)
					if request.session.session_key:
						key = request.session.session_key
						print("Login Session Key ")
						print(key)
						create_login_session_user(user , key)
					
					return redirect("user_dashboard")
			else:
				print("Users | Password Mismatched ")
				messages.error(request, 'Users | Password Mismatched')

		if request.method == "GET":
			print("Request is GET  ")

			fm = loginForm()
			context = {
				'user_login_form': fm , 
				'continue': False,
				'quiz_data' : get_detail_quiz(),
			}

		return render(request=request , template_name = 'core/login.html' , context = context)
	else:
		return redirect('user_dashboard')












@csrf_exempt
def user_registeration(request):
	context = {}
	if request.method == "POST":
		fm = SignUpForm(request.POST)
		if fm.is_valid():
			print("Yes data is valid ")
			fm.save()
			users = User.objects.get(pk = fm.instance.id)
			p = PlayerProfileModel.objects.create(users = users , cnic_name = users.first_name  ,  nic = "" ,mobile = fm.cleaned_data.get("mobile", ""),country = "" ,state = "",city = "" ,address = "")
			p.save()
			messages.success(request , "Account Created Successfully")

			msg_html = render_to_string('custom_authentication/register_email_template.html',
			{ 'first_name' : users.first_name  }
			) 

			url = "https://api.zeptomail.com/v1.1/email"
			payload = {
				'bounce_address':"bounce1@bounce.quiztainment.com.pk",
				"from": {"address": "noreply@quiztainment.com.pk"},
				"to": [
					{"email_address": {"address": users.email,
				"name":"quiztainment"}
				}],
				"subject":"Welcome Quiztainment.com",
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






			if request.user.is_authenticated:
				print("User is allready login")
				active_user_logout(request)
				uname = fm.cleaned_data['username']
				upass = fm.cleaned_data['password1']
				return new_user_direct_login(request= request , username= uname , password= upass)
			else:
				print("User is not login")
				# return redirect("login")
				uname = fm.cleaned_data['username']
				upass = fm.cleaned_data['password1']
				return new_user_direct_login(request= request , username= uname , password= upass)







# 			return redirect("login")
		else:
			context["form"] = fm
			messages.error(request , "Data is not valid")
	else:
		fm = SignUpForm()
		context = {
			'quiz_data' : get_detail_quiz(),
			"form" : fm,

		}
	return render(request=request , template_name = 'core/register.html' , context= context)




def payment_status_api(request):
	context = {}
	mdict = request.GET.urlencode()
	import ast
	from urllib.parse import parse_qs
	data = parse_qs(mdict)
	if data:
		z = QuizpaymentResponseAPI.objects.create(query_params = data )
		z.save()
		PaymentType = data.get("PaymentType")[0]
		TotalPrice = data.get("TotalPrice")[0]
		OrderId = data.get("OrderId")[0]
		ResultCode = data.get("ResultCode")[0]
		TxnId = data.get("TxnId")[0]
		Checksum = data.get("Checksum")[0]
		mdata = {
			"PaymentType"  :  data.get("PaymentType")[0],
			"TotalPrice"  :  data.get("TotalPrice")[0],
			"OrderId"  :  data.get("OrderId")[0],
			"ResultCode" :  data.get("ResultCode")[0],
			"TxnId"  :  data.get("TxnId")[0],
			"Checksum"  :  data.get("Checksum")[0],
		}
		if mdata.get("OrderId") and mdata.get("PaymentType")  :
			id = "QTPPA{}".format(mdata.get("OrderId"))
			if "QTPPA" in id:
				id = id.replace("QTPPA", "")
				id = int(id)
			if QuizstartModel.objects.filter(pk = id):
				quizstart = QuizstartModel.objects.get(pk = id)
				quizopen = QuizopenModel.objects.get(pk = quizstart.quizopen_id)
				u = QuizpaymentModel.objects.create(
					quizstart = quizstart,
					quizopen = quizopen,
					status = 'PAID',
					payment_type_value = str(mdata.get("PaymentType")),
					total_price = str(mdata.get("TotalPrice")),
					order_id = str(mdata.get("OrderId")),
					result_code = str(mdata.get("ResultCode")),
					txn_id = str(mdata.get("TxnId")),
					checksum = str(mdata.get("Checksum")),
					)
				u.save()
	return HttpResponse("success", content_type='application/json')




def take_exam(request):
	start_quiz_status = 0 
	user_questions_1 = 0
	context = {}
	context["user_questions_1"] = user_questions_1
	mdict = request.GET.urlencode()
	import ast
	mdict = mdict.replace("amp%3B", "")
	from urllib.parse import parse_qs
	data = parse_qs(mdict)
	if data:
		order_id = data.get("order_id")[0]
		transaction_id = data.get("transaction_id")[0]
		mdata = {
			"order_id"  :  data.get("order_id")[0],
			"transaction_id"  :  data.get("transaction_id")[0],
		}
		if mdata.get("order_id"):
			order_id = str(mdata.get("order_id"))
			if "QTPPA" in order_id:
				context["order_id"] = order_id
				context["transaction_id"] = mdata.get("transaction_id")
				order_id = order_id.replace("QTPPA", "")
				order_id = int(order_id)
				if QuizpaymentModel.objects.filter(quizstart_id = order_id , status = 'PAID'):
					quizpayment = QuizpaymentModel.objects.get(quizstart_id  = order_id , status = 'PAID')
					if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
						quizstart = QuizstartModel.objects.get( pk = quizpayment.quizstart.id , users_id = request.user.id)
						if QuizopenModel.objects.filter(  end_date_time__gt= datetime.now() ,    pk =  quizstart.quizopen.id ):
							quizopen = QuizopenModel.objects.get( end_date_time__gt= datetime.now() , pk =  quizstart.quizopen.id , status = 'OPENED' )
							if quizopen.status == 'OPENED':
								if request.POST:
									print()
									if AssignedquizModel.objects.filter( users_id = request.user.id  ,   quizstart_id = order_id):
										start_quiz_status = 3
										assinged_quiz_remainging_list = AssignedquizModel.objects.filter(   Q(quizstart_id =  quizstart.id) &   ~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
										# assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
										if assinged_quiz_remainging_list:
											assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id = order_id).count()
											if assignedquiz_count > len(assinged_quiz_remainging_list):
												print("")
												messages.success(request, " You have Remaining Quiz ")
												start_quiz_status = 4
												user_questions_1 = assinged_quiz_remainging_list[0].id
												context["user_questions_1"] = user_questions_1
											elif assignedquiz_count == len(assinged_quiz_remainging_list):
												user_questions_1 = assinged_quiz_remainging_list[0].id
												context["user_questions_1"] = user_questions_1
												start_quiz_status = 3
												delta = {}
												quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
												if quizstart.user_quiz_end_time> datetime.now():
													print("call timer function ")
													delta = differnet_date_time_(quizstart.user_quiz_end_time)
												context["quiz_time"] =  {
												"user_quiz_start_time" : quizstart.user_quiz_start_time,
												"user_quiz_end_time" : quizstart.user_quiz_end_time,
												"duration_hour" : delta.get("hour") or 0,
												"duration_mintues" :delta.get("mins") or 0,
												"duration_seconds" : delta.get("sec") or 0,

												}

										else:
											print("This Qestions Set Has been Dome. ")
											messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
											start_quiz_status = 5
									else:
										print("Created Questions. ")
										messages.success(request, " Created Questions ")

										quiz_numbers = quizopen.quiz_numbers
										quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
										if quiz_numbers > 0:
											question_loop = QuestionModel.objects.all().order_by('?')[:quiz_numbers]
											for i in question_loop:
												question = QuestionModel.objects.get(pk = i.id)
												user_assigned_quiz = AssignedquizModel.objects.create(
												quizstart = quizstart , 
												users =  request.user,
												quizopen =  quizopen,
												question =   question,
												correct_answer =  question.option_correct,
												ip_address =  quizstart.ip_address,
												)
												quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
												start_quiz_status = 3
												user_questions_1 = AssignedquizModel.objects.filter(quizstart = quizstart , users =  request.user).order_by('id').first()
												context["user_questions_1"] = user_questions_1

											delta = {}
											if quizstart.user_quiz_end_time:
												if quizstart.user_quiz_end_time> datetime.now():
													print("call timer function ")
													delta = differnet_date_time_(quizstart.user_quiz_end_time)
											context["quiz_time"] =  {
											"user_quiz_start_time" : quizstart.user_quiz_start_time or "",
											"user_quiz_end_time" : quizstart.user_quiz_end_time or "",
											"duration_hour" : delta.get("hour") or 0,
											"duration_mintues" :delta.get("mins") or 0,
											"duration_seconds" : delta.get("sec") or 0,

											}
								elif request.GET:
									if AssignedquizModel.objects.filter(quizstart_id = order_id):
										start_quiz_status = 1
										assinged_quiz_remainging_list = AssignedquizModel.objects.filter(   Q(quizstart_id =  quizstart.id) &   ~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))

										# assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
										if assinged_quiz_remainging_list:
											assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id = order_id).count()
											if assignedquiz_count > len(assinged_quiz_remainging_list):
												print("")
												start_quiz_status = 4
												context["start_quiz_status"] = start_quiz_status

												user_questions_1 = assinged_quiz_remainging_list[0].id
												context["user_questions_1"] = user_questions_1
											elif assignedquiz_count == len(assinged_quiz_remainging_list):
												start_quiz_status = 3
												context["start_quiz_status"] = start_quiz_status
												user_questions_1 = assinged_quiz_remainging_list[0].id

												delta = {}
												if quizstart.user_quiz_end_time> datetime.now():
													print("call timer function ")
													delta = differnet_date_time_(quizstart.user_quiz_end_time)
												context["quiz_time"] =  {
												"user_quiz_start_time" : quizstart.user_quiz_start_time,
												"user_quiz_end_time" : quizstart.user_quiz_end_time,
												"duration_hour" : delta.get("hour") or 0,
												"duration_mintues" :delta.get("mins") or 0,
												"duration_seconds" : delta.get("sec") or 0,

												}


										else:
											print("This Qestions Set Has been Dome. ")
											messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
											start_quiz_status = 5
											context["start_quiz_status"] = start_quiz_status

									else:
										print("Questions are not assigned Yed. ")
										start_quiz_status = 1
						else:
							messages.success(request , "This Quiz no more available")
					else:
						messages.success(request , "Start Quiz ID Not Found")

				else:
					print("  QuizpaymentModel ")
					messages.success(request , "Please Wait  ")

	context["start_quiz_status"] = start_quiz_status
	context["user_questions_1"] = user_questions_1

	return render(request=request , template_name = 'userdashboard/user_quiz_start.html'  ,context= context )






	# return render(request=request , template_name = 'core/payment_status_api.html'  ,context= context )




	# quizstart_id = request.GET.get("order_id") or ""
	# transaction_id = request.GET.get("amp;transaction_id") or ""
	# context = {}
	# start_quiz_status  = 0
	# if request.user.is_authenticated:
	# 	if request.POST:
	# 		print("Generate Quiz For Yours.")
	# 		if QuizpaymentModel.objects.filter(pk = 2):
	# 			quizpayment = QuizpaymentModel.objects.get(pk = 2 , users_id = request.user.id, status = 'PAID')
	# 			if quizpayment.payment_game_status == 'UNPLAYED':
	# 				if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id ):
	# 					print("Quiz Statement You Can Assigned Quiz to This Yours.")
	# 					quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id )
	# 					if QuizopenModel.objects.filter(pk = quizstart.quizopen.id ):
	# 						quizopen = QuizopenModel.objects.get(pk = quizstart.quizopen.id )

	# 						quiz_numbers = quizopen.quiz_numbers

	# 						if quiz_numbers > 0:
	# 							question_loop = QuestionModel.objects.all()[:5]

	# 							for i in question_loop:
	# 								question = QuestionModel.objects.get(pk = i.id)
	# 								user_assigned_quiz = AssignedquizModel.objects.create(
	# 								quizstart = quizstart , 
	# 								users =  request.user,
	# 								quizopen =  quizopen,
	# 								question =   question,
	# 								correct_answer =  question.option_correct,
	# 								ip_address =  quizstart.ip_address,
	# 								)
	# 								start_quiz_status = 3
	# 								messages.success(request , " Assgined Quiz is ready ")
	# 						else:
	# 							messages.success(request , " quiz_numbers < 0  ")
	# 					else:
	# 						messages.success(request , " QuizopenModel Not Matched.  ")
	# 				else:
	# 					messages.success(request , " QuizstartModel Not Matched.  ")
	# 			else:
	# 				messages.success(request , " payment_game_status is not UNPIAD.  ")
	# 		else:
	# 			messages.success(request , " QuizpaymentModel is not matched.  ")
	# 	else:
	# 		print("GET Requeset")
	# 		if QuizpaymentModel.objects.filter(pk = 2):
	# 			quizpayment = QuizpaymentModel.objects.get(pk = 2 , users_id = request.user.id, status = 'PAID')
	# 			if quizpayment.payment_game_status == 'UNPLAYED':
	# 				print("you can attend this quiz. ")
	# 				start_quiz_status = 1
	# 				messages.success(request , " you can attend this quiz ")
	# 			else:
	# 				messages.success(request , " Sorry can attend this quiz ")
	# 				start_quiz_status = 0
	# else:
	# 	return redirect("home")
	# context["start_quiz_status"] = start_quiz_status
	# context["quizstart_id"] = quizstart_id
	# context["transaction_id"] = transaction_id

	# return render(request=request , template_name = 'userdashboard/user_quiz_start.html'  ,context= context )




def differnet_date_time_(date_time_input):
	delta = date_time_input -  datetime.now()
	hour = 0
	mins = 0
	sec = 0
	if delta:
		totalMinute, second = divmod(delta.seconds, 60)
		hour, minute = divmod(totalMinute, 60)
		hour = hour
		mins =   totalMinute
		sec = second
	data = {"hour" : hour ,  "mins": mins , "sec" : sec}
	return data







def generate_256Hashcode_checksum_varified(id , open_quiz_code ,  payment_value ):
	payment_link = None
	if id and open_quiz_code and  payment_value:
		import hmac
		import hashlib
		secret_key = b"E3DC8F93C49E386B" # sendBox Secret Key
		production_secret_key = b"DE25E2CBE85C415E" # Production Secret Key

		id = "QTPPA{}".format(id)
		item = open_quiz_code
		amount = payment_value
		total_params = "Link:{}:{}:{}".format(id , item , amount)
		total_params = total_params.encode('utf-8')
		chcksum = hmac.new(production_secret_key, total_params, hashlib.sha256).hexdigest()
		print("signature = {0}".format(chcksum))
		if chcksum:
			payment_sandbox_url = "https://pay-sandbox.link.com.pk/?" # SendBox
			payment_production_url = "https://payin-pwa.link.com.pk/?"

			api_key = """api_key=43AF0AB3C51C82B2BA17E483F5C007FA&""" #sendBox Api Key
			production_api_key = """api_key=D02C6AF05C56A71CC89EF5468D317277&"""
			merchant_id  = """merchant_id={}&item={}&amount={}&""".format(id, item, amount )
			checksum = """checksum={}""".format(chcksum)
			payment_link = payment_production_url + production_api_key +  merchant_id + checksum
	return payment_link






def get_detail_quiz():
	quiz_open = QuizopenModel.objects.filter(Q(end_date_time__gt = datetime.now() , status = 'OPENED'))
	quiz_records = {}
	if quiz_open:
		for i in quiz_open:
			quiz_records = {
				"quiz_id" : i.id,
				"quiz_name" : i.quiz_name,
				"price_name" : i.price_name,
				"quiz_payment" : i.quiz_payment,
				"start_date_time" : i.start_date_time.strftime("%d-%m-%Y"),
				"end_date_time" : i.end_date_time.strftime("%d-%m-%Y"),
				"duation_time" : i.duation_time,
				"quiz_numbers" : i.quiz_numbers}

	return quiz_records
	








def new_user_direct_login(request , username , password):
	print("We are in new_user_direct_login")
	uname = username
	upass = password
	if uname and upass:
		user = authenticate(username=uname, password=upass)
		if user is not None:
			muser = User.objects.get(username = uname)
			print("muser User Found successfull " , muser)
			if UserLoginSession.objects.filter(users = muser):
				print(" UserLoginSession Found  ")
			else:
				print(" UserLoginSession User Not Found. ")
				dj_login(request, user)
				if request.session.session_key:
					key = request.session.session_key
					print("Login Session Key ")
					print(key)
					UserLoginSession.objects.create(users = user , session_key_id = key)
					print(" create_login_session_user - create_login_session_user ")
				# 	quiz_open = QuizopenModel.objects.filter(Q(end_date_time__gt = datetime.now() , status = 'OPENED'))
				# 	if quiz_open:
				# 		print(" quiz_open quiz_open quiz_open  "  , quiz_open[0].id)
				# 		quiz_open_id_value =  quiz_open[0].id
				# 		if QuizopenModel.objects.filter(pk=quiz_open_id_value,end_date_time__gt = datetime.now(), status = 'OPENED').exists():
				# 			users =  User.objects.get(id = request.user.id)
				# 			quizopen = QuizopenModel.objects.get(pk = quiz_open_id_value)
				# 			# context["quiz_name"] = quizopen.quiz_name
				# 			# context["quiz_pic"] = quizopen.quiz_name
				# 			print("Yes record exist. ")
				# 			u = QuizstartModel.objects.create(users = users , quizopen = quizopen ,  
				# 			ip_address  =  get_client_ip(request=request) )
				# 			u.save()
				# 			payment_link = generate_256Hashcode(u.id , u.quizopen.id,  u.quizopen.quiz_payment )
				# 			if payment_link:
				# 				print("Pyament link Genrated. ")
				# 				QuizstartModel.objects.filter(pk=u.id).update(payment_link_generated= payment_link )
				# 				return redirect("paid_payment", u.id)
				# 		else:
				# 			print("Sorry Quiz is closed or not available. ")
				# 			messages.info(request,  "This Quiz is not More Available")
					return redirect("home")




def create_login_session_user(user,key):
	UserLoginSession.objects.create(users = user , session_key_id = key)




def active_user_logout(request):
	print("active_user_logout active_user_logout ")
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
	
	
	
	
def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip




def generate_256Hashcode(id , open_quiz_code ,  payment_value ):
	payment_link = None
	if id and open_quiz_code and  payment_value:
		import hmac
		import hashlib
		secret_key = b"E3DC8F93C49E386B" # sendBox Secret Key
		production_secret_key = b"DE25E2CBE85C415E" # Production Secret Key
		original_id = id
		id = "QTPPA{}".format(id)
		item = open_quiz_code
		amount = payment_value
		total_params = "Link:{}:{}:{}".format(id , item , amount)
		total_params = total_params.encode('utf-8')
		chcksum = hmac.new(production_secret_key, total_params, hashlib.sha256).hexdigest()
		print("signature = {0}".format(chcksum))
		if chcksum:
			payment_sandbox_url = "https://pay-sandbox.link.com.pk/?" # SendBox
			payment_production_url = "https://payin-pwa.link.com.pk/?"
			api_key = """api_key=43AF0AB3C51C82B2BA17E483F5C007FA&""" #sendBox Api Key
			production_api_key = """api_key=D02C6AF05C56A71CC89EF5468D317277&"""
			merchant_id  = """merchant_id={}&item={}&amount={}&""".format(id, item, amount )
			checksum_original = chcksum
			checksum = """checksum={}""".format(chcksum)
			payment_link = payment_production_url + production_api_key +  merchant_id + checksum
			QuizstartModel.objects.filter(pk=original_id).update(checksum= checksum_original )
	return payment_link


# def page_not_found(request):
#     context = {}
#     return render(request, 'core/404.html', context, status=404)









def direct_take_exam(request , order_id):
	start_quiz_status = 0 
	user_questions_1 = 0
	context = {}
	context["user_questions_1"] = user_questions_1
	import ast
	from urllib.parse import parse_qs
	if QuizpaymentModel.objects.filter(quizstart_id = order_id , status = 'PAID'):
		quizpayment = QuizpaymentModel.objects.get(quizstart_id  = order_id , status = 'PAID')
		if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
			quizstart = QuizstartModel.objects.get( pk = quizpayment.quizstart.id , users_id = request.user.id)
			if QuizopenModel.objects.filter(  end_date_time__gt= datetime.now() ,    pk =  quizstart.quizopen.id ):
				quizopen = QuizopenModel.objects.get( end_date_time__gt= datetime.now() , pk =  quizstart.quizopen.id , status = 'OPENED' )
				if quizopen.status == 'OPENED':
					if request.method == 'POST':
						if AssignedquizModel.objects.filter( users_id = request.user.id  ,   quizstart_id = order_id):
							start_quiz_status = 3
							assinged_quiz_remainging_list = AssignedquizModel.objects.filter(   Q(quizstart_id =  quizstart.id) &   ~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
							# assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
							if assinged_quiz_remainging_list:
								assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id = order_id).count()
								if assignedquiz_count > len(assinged_quiz_remainging_list):
									print("")
									messages.success(request, " You have Remaining Quiz ")
									start_quiz_status = 4
									user_questions_1 = assinged_quiz_remainging_list[0].id
									context["user_questions_1"] = user_questions_1
								elif assignedquiz_count == len(assinged_quiz_remainging_list):
									user_questions_1 = assinged_quiz_remainging_list[0].id
									context["user_questions_1"] = user_questions_1
									start_quiz_status = 3
									delta = {}
									quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
									if quizstart.user_quiz_end_time> datetime.now():
										print("call timer function ")
										delta = differnet_date_time_(quizstart.user_quiz_end_time)
									context["quiz_time"] =  {
									"user_quiz_start_time" : quizstart.user_quiz_start_time,
									"user_quiz_end_time" : quizstart.user_quiz_end_time,
									"duration_hour" : delta.get("hour") or 0,
									"duration_mintues" :delta.get("mins") or 0,
									"duration_seconds" : delta.get("sec") or 0,

									}

							else:
								print("This Qestions Set Has been Dome. ")
								messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
								start_quiz_status = 5
						else:
							print("Created Questions. ")
							messages.success(request, " Created Questions ")

							quiz_numbers = quizopen.quiz_numbers
							quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
							if quiz_numbers > 0:
								question_loop = QuestionModel.objects.all().order_by('?')[:quiz_numbers]
								for i in question_loop:
									question = QuestionModel.objects.get(pk = i.id)
									user_assigned_quiz = AssignedquizModel.objects.create(
									quizstart = quizstart , 
									users =  request.user,
									quizopen =  quizopen,
									question =   question,
									correct_answer =  question.option_correct,
									ip_address =  quizstart.ip_address,
									)
									quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
									start_quiz_status = 3
									user_questions_1 = AssignedquizModel.objects.filter(quizstart = quizstart , users =  request.user).order_by('id').first()
									context["user_questions_1"] = user_questions_1

								delta = {}
								if quizstart.user_quiz_end_time:
									if quizstart.user_quiz_end_time> datetime.now():
										print("call timer function ")
										delta = differnet_date_time_(quizstart.user_quiz_end_time)
								context["quiz_time"] =  {
								"user_quiz_start_time" : quizstart.user_quiz_start_time or "",
								"user_quiz_end_time" : quizstart.user_quiz_end_time or "",
								"duration_hour" : delta.get("hour") or 0,
								"duration_mintues" :delta.get("mins") or 0,
								"duration_seconds" : delta.get("sec") or 0,

								}
					if request.method == 'GET':
						print("Request IS Get.. ")

						if AssignedquizModel.objects.filter(quizstart_id = order_id):
							print("Request IS Get..  AssignedquizModel   ")

							start_quiz_status = 1
							assinged_quiz_remainging_list = AssignedquizModel.objects.filter(   Q(quizstart_id =  quizstart.id) &   ~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))

							# assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
							if assinged_quiz_remainging_list:
								assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id = order_id).count()
								if assignedquiz_count > len(assinged_quiz_remainging_list):
									print("")
									start_quiz_status = 4
									context["start_quiz_status"] = start_quiz_status

									user_questions_1 = assinged_quiz_remainging_list[0].id
									context["user_questions_1"] = user_questions_1
								elif assignedquiz_count == len(assinged_quiz_remainging_list):
									start_quiz_status = 3
									context["start_quiz_status"] = start_quiz_status
									user_questions_1 = assinged_quiz_remainging_list[0].id

									delta = {}
									if quizstart.user_quiz_end_time> datetime.now():
										print("call timer function ")
										delta = differnet_date_time_(quizstart.user_quiz_end_time)
									context["quiz_time"] =  {
									"user_quiz_start_time" : quizstart.user_quiz_start_time,
									"user_quiz_end_time" : quizstart.user_quiz_end_time,
									"duration_hour" : delta.get("hour") or 0,
									"duration_mintues" :delta.get("mins") or 0,
									"duration_seconds" : delta.get("sec") or 0,

									}


							else:
								print("This Qestions Set Has been Dome. ")
								messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
								start_quiz_status = 5
								context["start_quiz_status"] = start_quiz_status

						else:
							print("Questions are not assigned Yed. ")
							start_quiz_status = 1
					print("Testing Without GETPOST")
			else:
				messages.success(request , "This Quiz no more available")
		else:
			messages.success(request , "Start Quiz ID Not Found")

	else:
		print("  QuizpaymentModel ")
		messages.success(request , "Please Wait  ")

	context["start_quiz_status"] = start_quiz_status
	context["user_questions_1"] = user_questions_1

	return render(request=request , template_name = 'userdashboard/user_quiz_start.html'  ,context= context )







