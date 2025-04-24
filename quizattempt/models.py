from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from quizstart.models import QuizstartModel
from quizopen.models import QuizopenModel
from qestions.models import QuestionModel
from assigned_quiz.models import AssignedquizModel

from django.urls import reverse
STATUS = (
	('SKIPPED','SKIPPED'),
	('SUBMITTED','SUBMITTED'),
)

class QuizattemptModel(models.Model):
	assignedquiz = models.ForeignKey(AssignedquizModel, on_delete=models.CASCADE)
	submitted_answer = models.CharField(max_length=1055, null=True, blank=True)
	compared_answer = models.CharField(max_length=1055, null=True, blank=True)
	status = models.CharField(max_length=1055, choices=STATUS ,   null=True, blank=True)
	ip_address = models.CharField(max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.id)




