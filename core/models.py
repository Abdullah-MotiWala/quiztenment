from django.db import models
from django.utils.timezone import now


from core.celery_task import   sending_email_all_user , sending_email_all_user_paid




class DummyDataDisplayModel(models.Model):
	choose_users = models.CharField(max_length=1055,   null=True, blank=True)
	user_satisfaction_rate = models.CharField(max_length=1055,   null=True, blank=True)
	user_growth_rate = models.CharField(max_length=1055,   null=True, blank=True)
	next_segment = models.CharField(max_length=1055,   null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)
	def __str__(self):
		return str( self.pk)




class SendEmailAllUserModel(models.Model):
	start = models.CharField(max_length=1055,   null=True, blank=True)
	end = models.CharField(max_length=1055,   null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)

	def save(self, *args, **kwargs):
		print("Save Data Called.")
		super(SendEmailAllUserModel, self).save(*args, **kwargs)
		sending_email_all_user(int(self.start) , int(self.end))
		print("EMail Send. ")




class SendEmailAllUserPaidModel(models.Model):
	start = models.CharField(max_length=1055,   null=True, blank=True)
	end = models.CharField(max_length=1055,   null=True, blank=True)
	creation = models.DateTimeField(default=now, editable=False)

	def save(self, *args, **kwargs):
		print("Save Data Called.")
		super(SendEmailAllUserPaidModel, self).save(*args, **kwargs)
		sending_email_all_user_paid(int(self.start) , int(self.end))
		print(" SendEmailAllUserPaidModel EMail Send. ")


	def __str__(self):
		return str( self.pk)











