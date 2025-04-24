from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime
from django.urls import reverse
from quizopen.models import QuizopenModel

QUIZOPEN_STATUS = (
	('CLOSED','CLOSED'),
	('CANCELLED','CANCELLED'),
	('OPENED','OPENED'),
)

PAYMENT_STATUS = (
	('PAID','PAID'),
	('UNPAID','UNPAID'),
)

PYAMENT_GAME_STATUS = (
	('PLAYED','PLAYED'),
	('UNPLAYED','UNPLAYED'),
)

class QuizUINModel(models.Model):
    UIN = models.CharField(max_length=20, unique=True)  
    attempts = models.PositiveIntegerField(default=0)
    updation = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.UIN} - Attempts: {self.attempts}"  

class QuizstartModel(models.Model):
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	payment_game_status = models.CharField(max_length=1055, choices= PYAMENT_GAME_STATUS ,    default='UNPLAYED' ,  null=True, blank=True)
	payment_status = models.CharField(max_length=1055, choices= PAYMENT_STATUS , default='UNPAID'  ,  null=True, blank=True)
	ip_address = models.CharField(max_length=1055, null=True, blank=True)
	payment_link_generated = models.CharField(max_length=1055, null=True, blank=True)

	user_quiz_start_time = models.DateTimeField(null = True , blank  = True )
	user_quiz_end_time = models.DateTimeField(null = True , blank  = True ,)
	checksum = models.CharField(max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)



	# def save(self, *args, **kwargs):
	# 	quiz_start_time = self.quizopen.start_date_time
	# 	quiz_end_date_time = self.quizopen.end_date_time
	# 	quiz_duation_time = self.quizopen.duation_time
	# 	if quiz_start_time and quiz_end_date_time and quiz_duation_time:
	# 		print("Please Set Duraiton User Quiz.")
	# 		# self.user_quiz_start_time
	# 		# self.user_quiz_end_time

	# 	super(QuizstartModel, self).save(*args, **kwargs)





	def __str__(self):
		return str( self.id)