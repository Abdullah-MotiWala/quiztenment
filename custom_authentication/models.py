from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from quizpayment.models import QuizpaymentModel, QuizpaymentItsModel
from quizpayment.models import QuizstartModel
from quizopen.models import QuizopenModel
from django.contrib.auth.models import User
from qestions.models import QuestionModel
from assigned_quiz.models import AssignedquizModel
from quizattempt.models import QuizattemptModel
from quizresult.models import QuizresultModel
from django.db.models import Q
from django.db.models import Exists, OuterRef

from datetime import datetime
from datetime import timedelta

from django.urls import reverse

CATEGORY_CHOICES = [
    ("tech", "Technology"),
    ("science", "Science"),
    ("arts", "Arts"),
    ("business", "Business"),
    ("education", "Education"),
]


class PlayerProfileModel(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    cnic_name = models.CharField(max_length=1055, null=True, blank=True)
    nic = models.CharField(max_length=1055, null=True, blank=True)
    mobile = models.CharField(max_length=1055, null=True, blank=True)
    country = models.CharField(max_length=1055, null=True, blank=True)
    state = models.CharField(max_length=1055, null=True, blank=True)
    city = models.CharField(max_length=1055, null=True, blank=True)
    address = models.CharField(max_length=1055, null=True, blank=True)
    creation = models.DateTimeField(default=now, editable=False)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return str(self.pk)


# class PlayerDpModel(models.Model):
# 	users = models.OneToOneField(User, on_delete=models.CASCADE )
#  	picture = models.ImageField(upload_to="profile_images", blank=True)
# 	def __str__(self):
# 		return str( self.pk)


class UserLoginSession(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key_id = models.CharField(max_length=250, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    session_key_cookies = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.users

    class Meta:
        verbose_name = "UserLoginSession"
        verbose_name_plural = "UserLoginSession"
