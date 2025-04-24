from multiprocessing.context import assert_spawning
from django.shortcuts import render  
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from pydoc import render_doc
import datetime
from django.shortcuts import render , redirect
from qestions.models import QuestionModel
from quizopen.models import QuizopenModel
from quizresult.models import QuizresultModel
from quizstart.models import QuizstartModel
from quizwinner.models import QuizwinnerModel
from django.contrib.auth.models import User
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import QuizattemptModel
from quizpayment.models import QuizpaymentModel 
from django.contrib import messages
from django.db.models import Q
from django.db.models import Exists, OuterRef

import json

import io
from rest_framework.parsers import JSONParser
# from  quizpayment.serializers import ResponsepaymentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

import requests




# Create your views here.


def user_dashboard(request):
	context = {}
	product_list = []
	if request.user.is_authenticated:
		quiz_open  = QuizopenModel.objects.all()
		context = {
			"quiz_open" : quiz_open
		}
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/open_quiz.html'  ,context= context )


def open_quiz(request):
	context = {}
	product_list = []
	if request.user.is_authenticated:
		quiz_open  = QuizopenModel.objects.all()
		context = {
			"quiz_open" : quiz_open
		}
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/open_quiz.html'  ,context= context )


def start_quiz(request):
	context = {}
	product_list = []
	if request.user.is_authenticated:
		print("User is Loggin ")
		if request.POST:
			print(" start_quiz Req is post ")
			id = request.POST.get("open_quiz_id")
			print(" --  start_quiz  open_quiz_id  " , id)
			if QuizopenModel.objects.filter(pk=id, status = 'OPENED').exists():
				users =  User.objects.get(id = request.user.id)
				quizopen = QuizopenModel.objects.get(pk = id)
				print("Yes record exist. ")
				u = QuizstartModel.objects.create(users = users , quizopen = quizopen ,  
				ip_address  = get_client_ip(request=request) )
				u.save()
				payment_link = generate_256Hashcode(u.id , u.quizopen.id,  u.quizopen.quiz_payment )
				if payment_link:
					print("Pyament link Genrated. ")
					QuizstartModel.objects.filter(pk=u.id).update(payment_link_generated= payment_link )
					return redirect("paid_payment", u.id)

			else:
				print("Sorry Quiz is closed or not available. ")
				return redirect("open_quiz")
		else:
			print(" start_quiz req is Get")
			return redirect("open_quiz")

	else:
		print("user is not loggin")
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/start_quiz.html'  ,context= context )

def attempt_quiz(request , id ):
	context = {}
	if request.user.is_authenticated:
		print("User is Loggin ")
		return redirect("submit_quiz" , id)
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/attempt_quiz.html'  ,context= context )

def submit_quiz(request , id ):
	print(" submit_quiz - - - submit_quiz ")
	context = {}
	product_list = []
	if request.user.is_authenticated:
		user_select_option = request.POST.get("user_select_option")
		users =  User.objects.get(id = request.user.id)
		if AssignedquizModel.objects.filter(users = users , id = id):
			assinged_quized = AssignedquizModel.objects.get(users = users , id = id)
			messages.success(request, " AssignedquizModel")
			if QuizpaymentModel.objects.filter(quizstart_id = assinged_quized.quizstart.id , status = 'PAID'):
				messages.success(request, " QuizpaymentModel")
				quizpayment = QuizpaymentModel.objects.get(quizstart_id  = assinged_quized.quizstart.id , status = 'PAID')
				messages.success(request , " quizpayment {} ".format(quizpayment))
				if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
					quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
					messages.success(request, " QuizstartModel")
					if QuizopenModel.objects.filter(pk =  quizstart.quizopen.id ):
						messages.success(request, " QuizopenModel")
						quizopen = QuizopenModel.objects.get(pk =  quizstart.quizopen.id )
						if quizopen.status == 'OPENED':
							messages.success(request, "  OPENED ")
							if request.POST:
								print("POST")
								user_select_option =  0 
								if QuizattemptModel.objects.filter(Assignedquiz_id = assinged_quized.id):
									print(" This Quiz Already Submittted. ")
								else:
									print(" PLease Store This Quiz in Database. ")
									user_select_option = request.POST.get("user_select_option")
									if "submit" in request.POST and user_select_option:
										print("Please Submitted Code. ")
										status = "SUBMITTED"
										user_select_option = user_select_option
									elif "skip" in request.POST and user_select_option == 0 or user_select_option == None  or user_select_option == "":
										print("Please skip Code. ")
										user_select_option = 0
										status = "SKIPPED"
									check_answer = assinged_quized.correct_answer
									compared_answer = 0
									if check_answer == user_select_option:
										compared_answer = 1
									attmpt = QuizattemptModel.objects.create(
										assignedquiz = user_questions , 
										submitted_answer = user_select_option,
										compared_answer = compared_answer ,
										status = status , 	
										ip_address = get_client_ip(request=request)			
										)
									attmpt.save()
									assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
									if assinged_quiz_remainging_list:
										messages.success(request, "  assinged_quiz_remainging_list ")
										assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id =  quizstart.id , users_id = request.user.id ).count()
										messages.success(request, "assignedquiz_count  {}".format(assignedquiz_count))
										messages.success(request, "assinged_quiz_remainging_list  {}".format(len(assinged_quiz_remainging_list)))
										if assignedquiz_count > len(assinged_quiz_remainging_list):
											print("")
											messages.success(request, " Yo can Play Quiz ")
											messages.success(request, " You have Remaining Quiz ")
											user_questions = assinged_quiz_remainging_list[0]
										elif assignedquiz_count == len(assinged_quiz_remainging_list):
											messages.success(request, " All Question Are Remaining.  ")
											messages.success(request, " Yo can Play Quiz ")
											user_questions = 
										return redirect("submit_quiz" , assinged_quiz_remainging_list[0].id )
										print(" - - -  ")
									else:
										print(" - - - ")
										print("Uesr Has No More Question to attempt. ")
							else:
								print("GET")




		if request.POST:

			if "submit" in request.POST and user_select_option:
				print("Please Submitted Code. ")
				status = "SUBMITTED"
			elif "skip" in request.POST and user_select_option == 0 or user_select_option == None  or user_select_option == "":
				print("Please skip Code. ")
				user_select_option = 0
				status = "SKIPPED"
			print("Post Method")
			if  AssignedquizModel.objects.filter(users = users , id = id):

				user_questions = AssignedquizModel.objects.get(users = users , id = id)
				print(" ID  " , id )	
				print(" user_questions " , user_questions)	
				check_answer = user_questions.correct_answer
				compared_answer = 0
				if check_answer == user_select_option:
					compared_answer = 1
				attmpt = QuizattemptModel.objects.create(
					assignedquiz = user_questions , 
					submitted_answer = user_select_option,
					compared_answer = compared_answer ,
					status = status , 	
					ip_address = get_client_ip(request=request)			
					)
				attmpt.save()
				context["quiz"]  = user_questions

				user_questions_1 = AssignedquizModel.objects.filter(pk__gt=id).order_by('id').first()
				if  user_questions_1:
					return redirect("submit_quiz" , user_questions_1.id)
				else:
					print("No More Question Found.  ")
					last_attend = AssignedquizModel.objects.filter(id=id).order_by('id').first()
					print(" last_attend quiz id  ---  " , last_attend.quizstart.id )
					messages.success(request, "")

					context["quiz"]  = user_questions_1

					context["last_attend"]  = last_attend.quizstart.id 
		else:
			messages.success(request, "GET request")

			print(" Get Request ")
			print(" Login User ")

			if AssignedquizModel.objects.filter(users = users , id = id):
				assinged_quized = AssignedquizModel.objects.get(users = users , id = id)
				messages.success(request, " AssignedquizModel")
				if QuizpaymentModel.objects.filter(quizstart_id = assinged_quized.quizstart.id , status = 'PAID'):
					messages.success(request, " QuizpaymentModel")
					quizpayment = QuizpaymentModel.objects.get(quizstart_id  = assinged_quized.quizstart.id , status = 'PAID')
					messages.success(request , " quizpayment {} ".format(quizpayment))
					if QuizstartModel.objects.filter(pk = quizpayment.quizstart.id , users_id = request.user.id):
						quizstart = QuizstartModel.objects.get(pk = quizpayment.quizstart.id , users_id = request.user.id)
						messages.success(request, " QuizstartModel")

						if QuizopenModel.objects.filter(pk =  quizstart.quizopen.id ):
							messages.success(request, " QuizopenModel")
							quizopen = QuizopenModel.objects.get(pk =  quizstart.quizopen.id )
							if quizopen.status == 'OPENED':
								messages.success(request, "  OPENED ")

								assinged_quiz_remainging_list = AssignedquizModel.objects.filter(~Exists(QuizattemptModel.objects.filter(assignedquiz_id=OuterRef('pk'))))
								if assinged_quiz_remainging_list:
									messages.success(request, "  assinged_quiz_remainging_list ")
									assignedquiz_count = AssignedquizModel.objects.filter(quizstart_id =  quizstart.id , users_id = request.user.id ).count()
									messages.success(request, "assignedquiz_count  {}".format(assignedquiz_count))
									messages.success(request, "assinged_quiz_remainging_list  {}".format(len(assinged_quiz_remainging_list)))
									if assignedquiz_count > len(assinged_quiz_remainging_list):
										print("")
										messages.success(request, " Yo can Play Quiz ")
										messages.success(request, " You have Remaining Quiz ")
										user_questions = assinged_quiz_remainging_list[0]
										context["quiz"] = user_questions
									elif assignedquiz_count == len(assinged_quiz_remainging_list):
										messages.success(request, " All Question Are Remaining.  ")
										messages.success(request, " Yo can Play Quiz ")
										user_questions = assinged_quiz_remainging_list[0]

										context["quiz"] = user_questions
								else:
									context["quiz"] = []
									messages.success(request, "You have Already Submitted This Quiz Or Timeout.")
									print("This Qestions Set Has been Dome. ")
									messages.success(request, " You Have Already Attempt All Questions Againsted This ID Sessions ")
		context["submitted_result_button"] = []
	else:
		print("submit_quiz - user is not loggin")
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/submit_quiz.html'  ,context= context )



def skip_quiz(request):
	context = {}
	product_list = []
	if request.user.is_authenticated:
		quiz = AssignedquizModel.objects.get(pk = 1)
		print("skip_quiz - User is Loggin ")
		if request.POST:
			if "skip" in request.POST:
				print("YES SKIPP FOUND")
			else:
				print("Sorry Skipp Not Found. ")
			print("skip_quiz - Post")
			user_select_option = request.POST.get("user_select_option")
			print(" user_select_option value " , user_select_option)
		else:
			print("skip_quiz - req is Get")
		context = {
			"quiz" : quiz
		}
	else:
		print("skip_quiz - user is not loggin")
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/attempt_quiz.html'  ,context= context )


def result_board(request):
	context = {}
	product_list = []
	if request.user.is_authenticated:
		if request.POST:
			print()
		else:
			print("skip_quiz - req is Get")
		context = {
			"quiz" : {}
		}
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/result_board.html'  ,context= context )


def submit_quiz_result(request):
	context = {}
	product_list = []
	row = {}
	if request.user.is_authenticated:
		if request.POST:
			quiz_start_id = request.POST.get("quiz_start_id")
			print(" quiz_start_id " , quiz_start_id  )
			if quiz_start_id:
				users =  User.objects.get(id = request.user.id)
				quizstart = QuizstartModel.objects.get(users  = users , id = quiz_start_id)
				if quizstart:
					total_corrent_answer = 0
					total_attempt_answer = 0
					total_skipped_answer = 0
					total_assigned_answer = 0
					total_submitted_answer = 0
					m = AssignedquizModel.objects.filter(quizstart = quizstart , users = users)
					for i in m:
						print("------------")
						print(i.id)
						print(i.quizstart)
						print(i.users)
						print(i.quizopen)
						print(i.question)
						print(i.correct_answer)
						print(i.ip_address)
						print("------------")
						total_assigned_answer += 1
						attmpt =  QuizattemptModel.objects.get(assignedquiz_id = i.id)
						if attmpt:
							print(" Attemp Found ")
							total_attempt_answer += 1
							if attmpt.status == 'SKIPPED' and attmpt.submitted_answer == 0:
								total_skipped_answer += 1
							if attmpt.status == 'SUBMITTED' and attmpt.submitted_answer != 0:
								total_submitted_answer += 1
							if i.correct_answer == attmpt.submitted_answer:
								total_corrent_answer += 1
					print(" IF quizstart " , quizstart.quizopen.id)
					quizopen = QuizopenModel.objects.get(id = quizstart.quizopen.id , status = 'OPENED')
					r = QuizresultModel.objects.create(
						users = users ,
						quizopen = quizopen , 
						quizstart = quizstart , 
						user_time_duration = "" , 
						corrent_anwswer = total_corrent_answer , 
						skipped_anwswer = total_skipped_answer , 
						percantage = "" ,
						total_attempt_answer = total_attempt_answer,
						total_assigned_answer = total_assigned_answer,
						total_submitted_answer = total_submitted_answer,
					)
					r.save()
					print(". quizopen   r r  " , r )
					context["data"] = QuizresultModel.objects.get(id = r.id)
					print(" context  " , context )



			else:
				print(" quiz_start_id  is null - 0 ")
		else:
			print("generate_result_status - req is Get")
			return redirect("open_quiz")
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/submit_quiz_result.html'  ,context= context )


def paid_payment(request ,  id):
	print(" paid_payment id  "  , id)
	context = {}
	product_list = []
	if request.user.is_authenticated:
		link = ""
		q = QuizstartModel.objects.get(pk=id)
		link = q.payment_link_generated 

		# if request.POST:
		# 	print(" paid_payment  Post Method. ")
		# 	amount_value = request.POST.get("amount_value")
		# 	start_quiz_id = request.POST.get("start_quiz_id")
		# 	print("  amount_value " , amount_value)
		# 	print("  start_quiz_id " , start_quiz_id)
		# 	if QuizstartModel.objects.filter(id=start_quiz_id).exists():
		# 		print(" YEs  QuizstartModel  " , start_quiz_id )
		# 		quizstart = QuizstartModel.objects.get(pk=id)
		# 		users =  User.objects.get(id = request.user.id)
		# 		quizopen = QuizopenModel.objects.get(pk = quizstart.quizopen.id)
		# 		quizplayed = QuizpaymentModel.objects.create(
		# 		quizstart = quizstart , 
		# 		users = users,
		# 		quizopen = quizopen ,
		# 		ip_address = get_client_ip(request=request)			
		# 		)
		# 		quizplayed.save()
		# 		quizstart.payment_status = "PAID"
		# 		quizstart.save()
		# 		print("Created QuizpaymentModel --  " , QuizpaymentModel)
		# 		print("Updated  --  quizstart " )
		# 		create_user_quiz_slot(request= request ,  quiz_start_id = quizstart.id)
		# 		if create_user_quiz_slot:
		# 			return redirect("payment_successfull" , quizstart.id)
		# 	else:
		# 		print("Sorry Quiz Start does not exsit")
		# else:
		# 	print("paid_payment - req is Get" , id)
		context = {
			"link" : link
		}
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/paid_payment.html'  ,context= context )





def create_user_quiz_slot(request , quiz_start_id):
	return_id  = False
	if request.user.is_authenticated:
		if request.POST:
			quizstart = QuizstartModel.objects.get(id = quiz_start_id)
			if quizstart:
				quiz_num = quizstart.quizopen.quiz_numbers
				all_question = QuestionModel.objects.all().order_by("-id")[:quiz_num]
				users =  User.objects.get(id = request.user.id)
				for i in all_question:
					question = QuestionModel.objects.get(id = i.id)
					assigned_questions = AssignedquizModel.objects.create(
					quizstart =quizstart, 
					users = users ,
					quizopen = quizstart.quizopen , 
					question = question ,
					correct_answer = i.option_correct,
					ip_address =get_client_ip(request=request),
					)
					assigned_questions.save()
				else:
					if AssignedquizModel.objects.filter(users = users , quizstart =  quizstart).exists():
						print("Your Quiz is Ready")	
						return_id = True
	return return_id





def payment_successfull(request ,  id):
	print(" payment_successfull  id  "  , id)
	context = {}
	product_list = []
	if request.user.is_authenticated:
		users =  User.objects.get(id = request.user.id)
		
		quizstart = QuizstartModel.objects.get(id = id)
		user_assigned_quiz = AssignedquizModel.objects.filter(users = users , quizstart =  quizstart).order_by("id").first()
		if request.POST:
			print("  payment_successfull post ")
		else:
			print("payment_successfull - req is Get" , id)
			quizstart = QuizstartModel.objects.get(id = id)
			user_assigned_quiz = AssignedquizModel.objects.filter(users = users , quizstart =  quizstart).order_by("id").first()
		context = {
			"quiz_data" : quizstart,
			"assigned_questions_id" : user_assigned_quiz.id
		}
	else:
		return redirect("login")
	return render(request=request , template_name = 'userdashboard/payment_successfull.html'  ,context= context )



def test_payment(request):
	payment_url = "https://pay-sandbox.link.com.pk/?"
	api_key = "api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"
	merchant_id = "merchant_id = QT40010&" ## always update ,
	item = "item=test&" ## Test #    
	amount = "amount=1&"
	checksum = "checksum=6ccbb36f8f912d99eafc32832de85e23db6f738abad26797ce00a86c8aa5b5d6" 
	secrat_key = "E3DC8F93C49E386B"
	mrul = payment_url + api_key+ merchant_id + item  + amount + checksum
	context = {}
	data = {}
	
	

	# r = requests.post(mrul)
	if request.method == 'POST':
		print("request Post")
		headers = {'Content-Type': 'application/json'}

		payment_type = request.POST.get("payment_type")
		email_addr = request.POST.get("email_addr")
		mobile_number = request.POST.get("mobile_number")
		cnic = request.POST.get("cnic")

		data = {
			"payment_type" : payment_type,
			"email_addr" : email_addr,
			"mobile_number" : mobile_number,
			"cnic" : cnic,
		}		
		r = requests.post(mrul, data=data , verify=False)

		print("Records has been saved.")
		messages.success(request, "Thanku Record saved!")
		response = requests.post(
			mrul,
			data = data
		)
		context["r"] = response.text
		messages.success(request, response.text )
		print(response.text)
	else:
		print("Request id Get ")
	context = {
		"form" : {}
	}
	return render(request=request , template_name = 'userdashboard/test_payment.html'  ,context= context )





def now_diff(start_time , end_time):
	print(" now_diff ")
	print(" start_time" , start_time)
	print(" end_time" , end_time)
	delta = end_time  - start_time
	print(" delta now_diff = " , delta)
	return delta
	# return delta.total_seconds() / (60 * 60)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




# def payment_status_api(request):
# 	data = request.body
# 	if request.method == 'GET':
# 		return HttpResponse(data, content_type='application/json')
# 	else:
# 		return HttpResponse(data, content_type='application/json')

# # URL = 'http://www.quiztainment.com.pk/user/payment_status_api'
# # print(r.text)
# # if r:
# #     if r.text:
# #         print("yes Value Found. ")
# #     else:
# #         print("Sorry Value Not Found. ")
        





def payment_callback_api(request):
	id = request.GET.get('PaymentType')
	data = {
		"PaymentType" : id , 
		"TotalPrice" : id , 
		"OrderId" : id , 
		"ResultCode" : id , 
		"TxnId" : id , 
		"Checksum" : id , 
	}
	print("Records has been saved.")

	return HttpResponse(data, content_type='application/json')






def generate_256Hashcode(id , open_quiz_code ,  payment_value ):
	payment_link = None
	if id and open_quiz_code and  payment_value:
		import hmac
		import hashlib
		secret_key = b"E3DC8F93C49E386B"
		id = "QTP{}".format(id)
		item = open_quiz_code
		amount = payment_value
		total_params = "Link:{}:{}:{}".format(id , item , amount)
		total_params = total_params.encode('utf-8')
		chcksum = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
		print("signature = {0}".format(chcksum))
		if chcksum:
			payment_sandbox_url = "https://pay-sandbox.link.com.pk/?"
			api_key = """api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"""
			merchant_id  = """merchant_id={}&item={}&amount={}&""".format(id, item, amount )
			checksum = """checksum={}""".format(chcksum)
			payment_link = payment_sandbox_url + api_key +  merchant_id + checksum
	return payment_link



# def generate_payment_link(checksum , start_quiz_code, payment_value , open_quiz_code):
# 	p_link = None
# 	if checksum and id:
# 		id = "QT{}".format(id)
# 		signature = None
# 		import hmac
# 		import hashlib
# 		id = "QT{}".format(id)
# 		total_params = "Link:{}:test:2".format(id)
# 		total_params = b""+total_params
# 		signature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
# 		print("signature = {0}".format(signature))
# 		return p_link






# 	z = ResponsepaymentModel.objects.create(trx_id = "Test")
# 	z.save()
# 	z.id
# 	import hashlib
# 	a_string = "link:QTT{}:test:2".format(z.id)
# 	hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()
# 	print(hashed_string)
# 	payment_url = "https://pay-sandbox.link.com.pk/?"
# 	api_key = "api_key=43AF0AB3C51C82B2BA17E483F5C007FA&"
# 	merchant_id = "merchant_id=QTT{}&".format(z.id)
# 	item = "item=test&"
# 	amount = "amount=2&"
# 	checksum = "checksum=d5dd969a4bf05c2babcd52f58635fb0241acbfba19dfb62a21d03274835fea53"
# 	main_url = payment_url + api_key + merchant_id + item  + amount + checksum
# 	secrat_key = "E3DC8F93C49E386B"
# 	context = {}
# 	data = {}


# 	context = {
# 		"main_url"  : "https://pay-sandbox.link.com.pk/?api_key=43AF0AB3C51C82B2BA17E483F5C007FA&merchant_id=QT503&item=test&amount=2&checksum=6f81dcda4d92c866d769ae3cedbc8df23618a1922e66ce4fc2aabd11a9c2b206"
# 	}
# 	return render(request=request , template_name = 'core/index.html'  ,context= context )




