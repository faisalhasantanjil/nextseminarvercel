from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class SeminarForm(ModelForm):

    class Meta:
        model = Seminar
        exclude = ("organization",)


class UserInformationForm(ModelForm):

    class Meta:
        model = UserInformation
        exclude = ("user",)


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        exclude = ("user",)


class RegistrationForm(ModelForm):

    class Meta:
        model = Registration
        fields = '__all__'
