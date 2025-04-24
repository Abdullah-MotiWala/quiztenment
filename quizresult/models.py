from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from quizstart.models import QuizstartModel
from quizopen.models import QuizopenModel
from qestions.models import QuestionModel
from datetime import datetime  
from datetime import timedelta
from django.urls import reverse
from datetime import timedelta



STATUS = (
	('SKIPPED','SKIPPED'),
	('SUBMITTED','SUBMITTED'),
)

MARIT_STATUS = (
	('QUALIFIED','QUALIFIED'),
	('NOT-QUAILIFIED','NOT-QUAILIFIED'),
)

NEW_MARIT_STATUS = (
	('FREE','FREE'),
	('NONFREE','NONFREE'),
)



class QuizresultModel(models.Model):
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)	
	quizstart = models.ForeignKey(QuizstartModel, on_delete=models.CASCADE)
	user_time_duration = models.CharField(null=True, blank=True , max_length=1055 )
	user_time_duration_actual = models.DurationField(default=timedelta(seconds = 0) , null=True, blank=True , max_length=1055 )
	marit_status = models.CharField(max_length=100, choices=MARIT_STATUS, default='NOT-QUAILIFIED')
	new_status = models.CharField(max_length=100, choices=NEW_MARIT_STATUS, default='FREE')
	corrent_anwswer = models.IntegerField(default = 0, null=True, blank=True)
	skipped_anwswer = models.CharField(max_length=1055, null=True, blank=True)
	percantage = models.CharField(max_length=1055, null=True, blank=True)
	awnsers_percantage = models.FloatField(max_length=1055, null=True, blank=True)
	total_attempt_answer = models.CharField(max_length=1055, null=True, blank=True)
	total_assigned_answer = models.CharField(max_length=1055, null=True, blank=True)
	total_submitted_answer = models.CharField(max_length=1055, null=True, blank=True)
	final_score = models.CharField(max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)
	class Meta:
		print()
		# ordering = ['-final_score']

	def save(self, *args, **kwargs):
		self.total_assigned_answer = self.quizopen.quiz_numbers 
		if self.quizstart.user_quiz_start_time:
			user_start_time = self.quizstart.user_quiz_start_time
			delta = self.creation - user_start_time
			seconds = delta.seconds
			self.user_time_duration = seconds
			if self.corrent_anwswer and int(self.corrent_anwswer)>=15:
				print("You are quilifed. ")
				self.marit_status = 'QUALIFIED'
			else:
				print("Sorry you are not quailfied. ")
				self.marit_status = 'NOT-QUAILIFIED'
			self.awnsers_percantage = (int(self.corrent_anwswer) / int(self.total_assigned_answer)) * 100
			self.awnsers_percantage = round(self.awnsers_percantage, 2) 
			if self.awnsers_percantage and seconds:
				self.user_time_duration_actual = timedelta(seconds = int(seconds) ) 
				percantage = (self.awnsers_percantage / seconds) * 100
				if percantage:
					self.final_score =  round(percantage, 4)  
		super(QuizresultModel, self).save(*args, **kwargs)






	def __str__(self):
		return str( self.id)

