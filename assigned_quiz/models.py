from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from quizstart.models import QuizstartModel
from quizopen.models import QuizopenModel
from qestions.models import QuestionModel
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta


from django.urls import reverse
STATUS = (
	('SKIPPED','SKIPPED'),
	('SUBMITTED','SUBMITTED'),
)


class AssignedquizModel(models.Model):
	quizstart = models.ForeignKey(QuizstartModel, on_delete=models.CASCADE)
	users = models.ForeignKey(User, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
	correct_answer = models.CharField(max_length=1055, null=True, blank=True)
	ip_address = models.CharField(max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)



	def save(self, *args, **kwargs):
		if self.quizstart and self.quizopen:
			quiz_start = QuizstartModel.objects.get(pk = self.quizstart.id)
			if quiz_start and quiz_start.user_quiz_start_time == None:
				duation_time = str(self.quizopen.duation_time)
				if duation_time:
					duation_time  = duation_time.split(":")[1]
				quiz_start.user_quiz_start_time = self.creation
				quiz_start.user_quiz_end_time =   (self.creation + timedelta(minutes= int(duation_time)))
				quiz_start.save()
		super(AssignedquizModel, self).save(*args, **kwargs)



	def __str__(self):
		return str( self.id)




