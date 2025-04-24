from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from quizstart.models import QuizstartModel
from quizopen.models import QuizopenModel
from qestions.models import QuestionModel

from django.urls import reverse

STATUS = (
	('PAID','PAID'),
	('UNPAID','UNPAID'),
)



PYAMENT_GAME_STATUS = (
	('PLAYED','PLAYED'),
	('UNPLAYED','UNPLAYED'),
)




class QuizpaymentModel(models.Model):
	quizstart = models.ForeignKey(QuizstartModel, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	status = models.CharField(max_length=1055, choices= STATUS ,  default = 'UNPAID' ,   null=True, blank=True)
	payment_game_status = models.CharField(max_length=1055, choices= PYAMENT_GAME_STATUS ,  default = 'UNPLAYED'   ,  null=True, blank=True)
	payment_type_value = models.CharField( default = '6' ,  max_length=1055, null=True, blank=True)
	total_price = models.CharField(   max_length=1055, null=True, blank=True)
	order_id = models.CharField(  max_length=1055, null=True, blank=True)
	result_code = models.CharField( max_length=1055, null=True, blank=True)
	txn_id = models.CharField(  max_length=1055, null=True, blank=True)
	checksum = models.CharField( max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)





	def save(self, *args, **kwargs):
		if self.quizstart:
			quiz_start = QuizstartModel.objects.get(pk = self.quizstart.id)
			if quiz_start:
				quiz_start.payment_status = 'PAID'
				quiz_start.save()



		super(QuizpaymentModel, self).save(*args, **kwargs)






	def __str__(self):
		return str( self.id)



def now_diff(self):
    delta = datetime.now() - self.call_time
    return delta.total_seconds() / (60 * 60)



class QuizpaymentItsModel(models.Model):
	quizstart = models.ForeignKey(QuizstartModel, on_delete=models.CASCADE)
	quizopen = models.ForeignKey(QuizopenModel, on_delete=models.CASCADE)
	status = models.CharField(max_length=1055, choices= STATUS ,  default = 'UNPAID' ,   null=True, blank=True)
	payment_game_status = models.CharField(max_length=1055, choices= PYAMENT_GAME_STATUS ,  default = 'UNPLAYED'  ,  null=True, blank=True)

	ip_address = models.CharField(max_length=1055, null=True, blank=True)
	payment_type_value = models.CharField( default = '1' ,  max_length=1055, null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.id)







class QuizpaymentResponseAPI(models.Model):
	query_params = models.CharField(max_length=2055,   null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.id)







