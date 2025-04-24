from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , PasswordChangeForm , PasswordResetForm
from django.contrib.auth import authenticate , login  as dj_login , logout as dj_logout , update_session_auth_hash
from  custom_authentication.forms import SignUpForm , loginForm
from django.contrib import messages
from quizpayment.models import QuizpaymentModel  , QuizpaymentItsModel
from quizpayment.models import QuizstartModel
from quizopen.models import QuizopenModel
from django.contrib.auth.models import User  
from qestions.models import QuestionModel
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import  QuizattemptModel
from django.db.models import Q
from django.db.models import Exists, OuterRef



from django.contrib import messages
import json

import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse




# Create your views here.


def home(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/index.html'  ,context= context )


def about(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/about.html'  ,context= context )

def policy(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/policy.html'  ,context= context )


def terms(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/terms.html'  ,context= context )





def blog(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/blog.html'  ,context= context )



def faq(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/faq.html'  ,context= context )

def score_board(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/score_board.html'  ,context= context )

def contact_us(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/contact_us.html'  ,context= context )


contact_us


def open_quiz_list(request):
	context = {}
	product_list = []
	return render(request=request , template_name = 'core/index_open_quiz.html'  ,context= context )




def login(request):
	if not request.user.is_authenticated:
		context = {}
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
		return render(request=request , template_name = 'core/login.html' , context = context)
	return redirect("home")





def user_registeration(request):
	context = {}
	if request.method == "POST":
		fm = SignUpForm(request.POST)
		if fm.is_valid():
			print("Yes data is valid ")
			fm.save()
			messages.success(request , "Account Created Successfully")
			context =  {}
			return redirect("login")
		else:
			context["form"] = fm
			messages.error(request , "Data is not valid")
	else:
		fm = SignUpForm()
		context = {
			"form" : fm
		}
	return render(request=request , template_name = 'core/register.html' , context= context)




def payment_status_api(request):
	context = {}
	mdict = request.GET.urlencode()
	import ast
	mdict = mdict.replace("amp%3B", "")
	from urllib.parse import parse_qs
	data = parse_qs(mdict)
	if data:
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
		if mdata.get("OrderId"):
			id = "QTP{}".format(mdata.get("OrderId"))
			if "QTP" in id:
				id = id.replace("QTP", "")
				id = int(id)
			if QuizstartModel.objects.filter(pk = id):
				quizstart = QuizstartModel.objects.get(pk = id)
				quizopen = QuizopenModel.objects.get(pk = quizstart.quizopen_id)
				u = QuizpaymentModel.objects.create(
					quizstart = quizstart,
					quizopen = quizopen,
					status = 'PAID',
					)
				u.save()
	return HttpResponse("success", content_type='application/json')




def take_exam(request):
	start_quiz_status = 0 
	user_questions_1 = 0
	context = {}
	context["user_questions_1"] = ""
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
			if "QTP" in order_id:
				context["order_id"] = order_id
				context["transaction_id"] = mdata.get("transaction_id")
				order_id = order_id.replace("QTP", "")
				order_id = int(order_id)
				if AssignedquizModel.objects.filter(quizstart_id = order_id):
					if QuizpaymentModel.objects.filter(quizstart_id = order_id , status = 'PAID'):
						quizpayment = QuizpaymentModel.objects.get(quizstart_id  = order_id , status = 'PAID')
						if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
							quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
							if QuizopenModel.objects.filter(pk =  quizstart.quizopen.id ):
								quizopen = QuizopenModel.objects.get(pk =  quizstart.quizopen.id )
								if quizopen.status == 'OPENED':
									if request.POST:
										print()
										if AssignedquizModel.objects.filter(quizstart_id = order_id):
											print("Quiz Already Assigned Against This ID ")
											messages.success(request, "Quiz Already Assigned Against This ID")
											start_quiz_status = 3
										else:
											print("Created Questions. ")
											quiz_numbers = quizopen.quiz_numbers
											if quiz_numbers > 0:
												question_loop = QuestionModel.objects.all()[:5]
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
													start_quiz_status = 3
													user_questions_1 = AssignedquizModel.objects.filter(quizstart = quizstart , users =  request.user).order_by('id').first()
													context["user_questions_1"] = user_questions_1

									elif request.GET:












				if request.POST:
					print("Request POST ")



					if AssignedquizModel.objects.filter(quizstart_id = order_id):
						print("Quiz Already Assigned Against This ID ")
						messages.success(request, "Quiz Already Assigned Against This ID")
						start_quiz_status = 3
						quizattempts_list = QuizattemptModel.objects.select_related('assignedquiz')
						messages.success(request, quizattempts_list)

						 
					else:
						print("Quiz not Assigned Against This ID ")
						messages.success(request, " Quiz not Assigned Against This ID ")
						if QuizpaymentModel.objects.filter(quizstart_id = order_id , status = 'PAID'):
							quizpayment = QuizpaymentModel.objects.get(quizstart_id  = order_id , status = 'PAID')
							if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
								quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
								if QuizopenModel.objects.filter(pk =  quizstart.quizopen.id ):
									quizopen = QuizopenModel.objects.get(pk =  quizstart.quizopen.id )
									
									if quizopen.status == 'OPENED':
										quiz_numbers = quizopen.quiz_numbers
										if quiz_numbers > 0:
											question_loop = QuestionModel.objects.all()[:5]
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
												start_quiz_status = 3
												user_questions_1 = AssignedquizModel.objects.filter(quizstart = quizstart , users =  request.user).order_by('id').first()
												context["user_questions_1"] = user_questions_1


									else:
										messages.success(request , " You Can Not Play This Quiz  ")

				elif request.GET:
					if AssignedquizModel.objects.filter(quizstart_id = order_id):
						if QuizpaymentModel.objects.filter(quizstart_id = order_id , status = 'PAID'):
							quizpayment = QuizpaymentModel.objects.get(quizstart_id  = order_id , status = 'PAID')
							if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
								quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
								if QuizopenModel.objects.filter(pk =  quizstart.quizopen.id ):
									quizopen = QuizopenModel.objects.get(pk =  quizstart.quizopen.id )
									if quizopen.status == 'OPENED':
										print("Status Check")
										print("Quiz Already Assigned Against This ID ")
										messages.success(request, "Quiz Already Assigned Against This ID")
										start_quiz_status = 3
										assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
										if assinged_quiz_remainging_list:
											assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id = order_id).count()
											messages.success(request, "assignedquiz_count  {}".format(assignedquiz_count))
											messages.success(request, "assinged_quiz_remainging_list  {}".format(len(assinged_quiz_remainging_list)))
											if assignedquiz_count > len(assinged_quiz_remainging_list):
												print("")
												messages.success(request, " Yo can Play Quiz ")
												messages.success(request, " You have Remaining Quiz ")
												start_quiz_status = 4
												user_questions_1 = assinged_quiz_remainging_list[0].id
												context["user_questions_1"] = user_questions_1
												messages.success(request, " user_questions_1 {} ".format(user_questions_1))

											elif assignedquiz_count == len(assinged_quiz_remainging_list):
												messages.success(request, " All Question Are Remaining.  ")
												messages.success(request, " Yo can Play Quiz ")
												start_quiz_status = 3
										else:
											messages.success(request, "You have Already Submitted This Quiz Or Timeout.")
											print("This Qestions Set Has been Dome. ")
											messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
											start_quiz_status = 5

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



# def user_quiz_start(request):
# 	context = {}
# 	product_list = []
# 	if request.user.is_authenticated:
# 		print()
# 	else:
# 		return redirect("login")
# 	return render(request=request , template_name = 'userdashboard/user_quiz_start.html'  ,context= context )
