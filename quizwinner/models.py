from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from quizpayment.models import QuizpaymentModel  , QuizpaymentItsModel
from quizpayment.models import QuizstartModel
from quizopen.models import QuizopenModel
from django.contrib.auth.models import User  
from qestions.models import QuestionModel
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import  QuizattemptModel
from quizresult.models import QuizresultModel
from django.db.models import Q
from django.db.models import Exists, OuterRef

from datetime import datetime
from datetime import timedelta



from django.urls import reverse
STATUS = (
	('SKIPPED','SKIPPED'),
	('SUBMITTED','SUBMITTED'),
)

class QuizwinnerModel(models.Model):
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	quizresult = models.ForeignKey(QuizresultModel, on_delete=models.CASCADE)
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.id)



class QuizwinnerAnnoucementModel(models.Model):
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	creation = models.DateTimeField(default=now, editable=False)



	def save(self, *args, **kwargs):
		if QuizopenModel.objects.filter(pk = self.quizopen.id ,  status = 'OPENED'  ):
			quizopen = QuizopenModel.objects.filter(pk = self.quizopen.id , status = 'OPENED' )
			quizstart = QuizstartModel.objects.filter(quizopen_id = self.quizopen.id ,   payment_game_status =   'PLAYED' ,  payment_status = 'PAID')
			# for a in quizstart:
			# 	print("Get All quizstart Against This quizstart  ")
			# 	assignedquiz = AssignedquizModel.objects.filter(quizstart_id = a.id)
			# 	for b in assignedquiz:
			# 		if QuizattemptModel.objects.filter(assignedquiz_id = b.id):
			# 			print("Records Already Exsit")
			# 		else:
			# 			print("Please Created Skipp Records. ")
			# 			remain_quiz = QuizattemptModel.objects.create(
			# 			assignedquiz =   AssignedquizModel.objects.get(pk = b.id), 
			# 			submitted_answer = 0,
			# 			compared_answer = 0 ,
			# 			status = 'SKIPPED' ,
			# 			)
			# 			remain_quiz.save()
			# for aa in quizstart:
			# 	asigned_quiz_result = AssignedquizModel.objects.filter(quizstart_id = aa.id)
			# 	for bb in asigned_quiz_result:
			# 		quiz__result = QuizresultModel.objects.filter(quizstart_id = aa.id)
			# 		if quiz__result:
			# 			print("Result is Already Created. ")
			# 		else:
			# 			print("Please Create The Result. ")
			# 			quizattemptt = QuizattemptModel.objects.filter(assignedquiz_id = bb.id, corrent_anwswer__gte = 60 )
			# 			total_corrent_answer = 0
			# 			total_attempt_answer = 0
			# 			total_skipped_answer = 0
			# 			total_assigned_answer = 0
			# 			total_submitted_answer = 0
			# 			for i in quizattemptt:
			# 				print(" Attemp Found ")
			# 				total_attempt_answer += 1
			# 				if i.status == 'SKIPPED' and i.submitted_answer == 0:
			# 					total_skipped_answer += 1
			# 				if i.status == 'SUBMITTED' and i.submitted_answer != 0:
			# 					total_submitted_answer += 1
			# 				if i.compared_answer == i.submitted_answer:
			# 					total_corrent_answer += 1

			# 			result_quiz =  QuizresultModel.objects.create(
			# 			users =  User.objects.get(pk = bb.users_id),
			# 			quizopen =  QuizopenModel.objects.get(pk = aa.quizopen_id),
			# 			quizstart =  QuizstartModel.objects.get(pk = aa.id),
			# 			corrent_anwswer = total_corrent_answer,
			# 			skipped_anwswer =  total_skipped_answer,
			# 			total_attempt_answer = total_attempt_answer,
			# 			total_submitted_answer = total_submitted_answer,
			# 			)
			# 			result_quiz.save()
		
			if QuizresultModel.objects.filter(quizopen_id =  self.quizopen.id):
				result = QuizresultModel.objects.filter(quizopen_id =  self.quizopen.id , corrent_anwswer__gte = 60  ).order_by("-corrent_anwswer", "final_score")[:1]
				for z in result:
					result_quiz =  QuizwinnerModel.objects.create(
					users =  User.objects.get(pk = z.users_id),
					quizopen =  QuizopenModel.objects.get(pk = self.quizopen.id),
					quizresult =  QuizresultModel.objects.get(pk = z.id),
					)
					result_quiz.save()
		super(QuizwinnerAnnoucementModel, self).save(*args, **kwargs)






	def __str__(self):
		return str( self.id)

