from email import message
from django.contrib.auth.models import User

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserChangeForm,
)
from django import forms

from .models import PlayerProfileModel, CATEGORY_CHOICES
from django.db.models import Q

_CHOICES = [
    ("yes", ""),
]


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-sm "}),
    )
    password2 = forms.CharField(
        label="Confirm Password (Again)",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )
    mobile = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )
    first_name = forms.CharField(
        label="Full name",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )
    username = forms.CharField(
        label="User Name",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-sm "}),
    )
    username = forms.CharField(
        label="User Name",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-sm "}),
    )
    terms_condition = forms.BooleanField(
        label="Terms & Conditions",
        widget=forms.CheckboxInput(
            attrs={"required": "required", "checked": "checked"}
        ),
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Category",
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "mobile", "email"]
        labels = {
            "email": "Email Address",
            "username": "UserName",
            "first_name": "Full Name",
        }

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email


class loginForm(AuthenticationForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )
    username = forms.CharField(
        label="User Name",
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )

    class Meta:
        model = User
        fields = ["username"]


class PlayerProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlayerProfileForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:  # form is new
            print(" Form is new ")
        else:
            print(" Form is For Updated ")

    class Meta:
        model = PlayerProfileModel

        fields = ["cnic_name", "nic", "mobile", "country", "state", "city", "address"]
        widgets = {
            "cnic_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "required": "required",
                    "placeholder": "Enter Your Name",
                }
            ),
            "nic": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "type": "number",
                    "placeholder": "Enter Your NIC",
                }
            ),
            "mobile": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "type": "number",
                    "placeholder": "Enter Your Mobile",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "placeholder": "Enter Your Country",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "placeholder": "Enter Your State Ex Sindh",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "placeholder": "Enter Your City",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm ",
                    "required": "required",
                    "placeholder": "Address",
                }
            ),
        }


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Enter Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )
    new_password2 = forms.CharField(
        label="Confrimed Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm "}),
    )

    class Meta:
        model = PasswordChangeForm
        fields = ["old_password", "new_password1", "new_password2"]


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('picture' , )


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
    )
    nic = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm "}),
        label="Cnic/Passport Number",
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        # print("self request " , self.request.user)
        if self.instance:  # Ensure an instance exists
            try:
                user_profile = PlayerProfileModel.objects.get(users=self.instance)
                self.fields["phone"].initial = user_profile.mobile
                self.fields["nic"].initial = user_profile.nic
            except PlayerProfileModel.DoesNotExist:
                self.fields["phone"].initial = ""
                self.fields["nic"].initial = ""

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]
        exlude = ("password",)

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get("email")
        if User.objects.filter(Q(pk=self.instance.id), Q(email=email)).exists():
            print("Let The Email Store ")
        else:
            if User.objects.filter(Q(email=email)).exists():
                raise forms.ValidationError("Email Exsit with another Account ")
            else:
                print("You can store this Email ")

        return email

    def clean_username(self):
        # Get the username
        username = self.cleaned_data.get("username")
        if User.objects.filter(Q(pk=self.instance.id), Q(username=username)).exists():
            print("Let The username Store ")
        else:
            if User.objects.filter(Q(username=username)).exists():
                raise forms.ValidationError("UserName Exsit with another Account ")
            else:
                print("You can store this username ")

        return username

    # def clean_username(self):
    # 	if self.username is None or self.username == "":
    # 		print("User Name is null ")
    # 		self.username =  self.request.user
    # 	else:
    # 		print("User Name is Not Null ")
